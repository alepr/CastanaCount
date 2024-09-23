import geopandas as gpd 
from sqlalchemy import create_engine
import json
import pandas as pd
import ee 
import numpy as np
try:
    ee.Initialize()
except:
    ee.Authenticate(auth_mode="notebook")
    ee.Initialize()

config = {}
with open("pgDB", "r") as datos:
    for part in datos:
        key, value = part.strip().split("=")
        config[key] = value

con = create_engine(f"postgresql://{config["user"]}:{config["password"]}@{config["url"]}:{config["port"]}/{config["db"]}")
sql = """
        SELECT 
            geom AS "geometry", 
            "Nombre_Corto" AS "Nombre", 
            'TI' AS "dummy" 
        FROM 
            "public"."TerritoriosIndigenas"
        UNION
        SELECT 
            geom AS "geometry", 
            "Nombre_Corto" AS "Nombre", 
            'AP' AS "dummy" 
        FROM 
            "public"."APNacionales"
        UNION
        SELECT 
            geom AS "geometry", 
            "Nombre_Corto" AS "Nombre", 
            'AP' AS "dummy" 
        FROM 
            "public"."APDepartamentales"
        UNION
        SELECT 
            geom AS "geometry", 
            "Nombre_Corto" AS "Nombre", 
            'AP' AS "dummy" 
        FROM 
            "public"."APMunicipales"
        UNION
        SELECT 
            geom AS "geometry", 
            "Nombre", 
            'Municipio' AS "dummy" 
        FROM 
            "public"."Municipios-PND"
         """
corte = gpd.read_postgis(sql, con, geom_col="geometry").explode().dissolve("Nombre").reset_index()

gdf = gpd.read_file(r"D:\00_ACEAA\OneDrive - ACEAA\05_SIG\Pando\pando\pando.shp")
df = pd.read_csv(r"C:\Users\Alejandro\Downloads\PGIBT.csv")
df["Parcela"].unique()
shpFin = gdf[gdf["Parcela"].isin(df["Parcela"].unique())]

shpFin = shpFin.loc[:, ["Parcela", "geometry"]]
shpFin["dummy"] = "Comunidad con PGIBT"
shpFin.columns = ["Nombre", "geometry", "dummy"]

corte = pd.concat([corte, shpFin]).reset_index()
del gdf
del df
del shpFin
corte = corte.dissolve("Nombre").reset_index()

fcCorte = ee.FeatureCollection(json.loads(corte.to_json()))

Castaña1 = ee.Image('users/anmarkos/CASTANHA/Castanha_995_2024_06_03')
Castaña2 = ee.Image('users/anmarkos/CASTANHA/Castanha_99_2024_06_03')

ArbolesGrandes = Castaña1.eq(2).rename("Castana995Grande").selfMask().addBands(Castaña2.eq(2).rename("Castana99Grande").selfMask())
ArbolesPeq = Castaña1.eq(1).rename("Castana995Peq").selfMask().addBands(Castaña2.eq(1).rename("Castana99Peq").selfMask())
reduceArbGrandes = ArbolesGrandes.reduceRegions(collection=fcCorte, reducer=ee.Reducer.count(), scale=20, crs="EPSG:32719")
reduceArbPeq = ArbolesPeq.reduceRegions(collection=fcCorte, reducer=ee.Reducer.count(), scale=10, crs="EPSG:32719")

gdf = gpd.GeoDataFrame.from_features(reduceArbGrandes.getInfo())
gdf2 = gpd.GeoDataFrame.from_features(reduceArbPeq.getInfo())

gdfFinal = gdf.merge(gdf2)

gdfFinal = gdfFinal.loc[:, ["Nombre", "dummy", "Castana995Grande", "Castana995Peq", "Castana99Grande", "Castana99Peq"]]

gdfFinal.to_excel("CastanaCount.xlsx", index=False)


bolivia = ee.Image("projects/mapbiomas-public/assets/bolivia/collection2/mapbiomas_bolivia_collection2_integration_v1")

bolivia = bolivia.select("classification_2023")
areaBosque = ee.Image.pixelArea().divide(10000).updateMask(bolivia.eq(3))

reduceBosque = areaBosque.reduceRegions(collection=fcCorte, reducer=ee.Reducer.sum(), scale=30, crs="EPSG:32719")

gdf3 = gpd.GeoDataFrame.from_features(reduceBosque.getInfo())

gdfFinal = gdfFinal.merge(gdf3)      

trabajo_Final = gdfFinal.loc[:, ["Nombre", "dummy", "Castana995Grande", "Castana99Grande", "sum"]]
trabajo_Final.rename(columns={"sum":"AreaBosque"}, inplace=True)
trabajo_Final["ArbolesporHectarea995"] = trabajo_Final["Castana995Grande"]/trabajo_Final["AreaBosque"]
trabajo_Final["ArbolesporHectarea99"] = trabajo_Final["Castana99Grande"]/trabajo_Final["AreaBosque"]
trabajo_Final.rename(columns=dict(Castana995Grande="Castana995", Castana99Grande="Castana99"), inplace=True)
def cambiarFraccionProductores(x:float, gdf:gpd.GeoDataFrame=trabajo_Final):
    gdf.attrs["fraccionProductores"]=x
    gdf.attrs["fraccionNoProductores"]=1-x
    gdf.attrs["ProduccionMinima"] = 11.5
    gdf.attrs["ProduccionMaxima"] = 22.0257773123144
    gdf["ArbolesProductores995"]=gdf["Castana995"]* gdf.attrs["fraccionProductores"]
    gdf["ArbolesProductores99"]=gdf["Castana99"]* gdf.attrs["fraccionProductores"]
    gdf["MinimaAnual995"]=gdf["ArbolesProductores995"]* gdf.attrs["ProduccionMinima"]
    gdf["MaximaAnual995"]=gdf["ArbolesProductores995"]* gdf.attrs["ProduccionMaxima"]
    gdf["MinimaAnual99"]=gdf["ArbolesProductores99"]* gdf.attrs["ProduccionMinima"]
    gdf["MaximaAnual99"]=gdf["ArbolesProductores99"]* gdf.attrs["ProduccionMaxima"]
    gdf["MinimaAnualporha995"] = gdf["MinimaAnual995"]/gdf["AreaBosque"]
    gdf["MaximaAnualporha995"] = gdf["MaximaAnual995"]/gdf["AreaBosque"]
    gdf["MinimaAnualporha99"] = gdf["MinimaAnual99"]/gdf["AreaBosque"]
    gdf["MaximaAnualporha99"] = gdf["MaximaAnual99"]/gdf["AreaBosque"]
    gdf["MinimaAnualCaja995"] = gdf["MinimaAnual995"]/23
    gdf["MaximaAnualCaja995"] = gdf["MaximaAnual995"]/23
    gdf["MinimaAnualCaja99"] = gdf["MinimaAnual99"]/23
    gdf["MaximaAnualCaja99"] = gdf["MaximaAnual99"]/23
    gdf["MinimaAnualCajaporha995"] = gdf["MinimaAnualCaja995"]/gdf["AreaBosque"]
    gdf["MaximaAnualCajaporha995"] = gdf["MaximaAnualCaja995"]/gdf["AreaBosque"]
    gdf["MinimaAnualCajaporha99"] = gdf["MinimaAnualCaja99"]/gdf["AreaBosque"]
    gdf["MaximaAnualCajaporha99"] = gdf["MaximaAnualCaja99"]/gdf["AreaBosque"]
    return gdf
trabajo_Final = cambiarFraccionProductores(1, trabajo_Final)

list995 = [i for i in trabajo_Final.columns if i[-3:] == "995"]
list99 = [i for i in trabajo_Final.columns if i[:-2] == "99"]
otros = [i for i in trabajo_Final.columns if i[-3:] != "995" and i[-2:] != "99"]


with pd.ExcelWriter("CastanaProd.xlsx") as writer:

    for i in trabajo_Final.dummy.unique():
        tmp = trabajo_Final[trabajo_Final["dummy"]==i].copy()
        tmp = tmp.drop("dummy", axis=1)
        tmp.to_excel(writer, sheet_name=i, index=False)


