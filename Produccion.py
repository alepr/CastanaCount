import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_excel(r"CastanaProd.xlsx", sheet_name="TI")

fig = plt.figure(figsize=(20, 8))

ax1 = plt.subplot2grid(shape=(3,3), loc=(0,0))
ax2 = plt.subplot2grid(shape=(3,3), loc=(1,0), rowspan=2)
ax3 = plt.subplot2grid(shape=(3,3), loc=(0,1), rowspan=3)

plt.subplots_adjust(hspace=0)
sns.barplot(data=df, x="Nombre", y="ArbolesporHectarea99", ax=ax1)
sns.barplot(data=df, x="Nombre", y="Arboles Grandes", ax=ax2, label="Arboles Grandes")
sns.barplot(data=df, x="Nombre", y="Arboles Pequeños", ax=ax2, label= "Arboles Pequeños")
produccion = pd.melt(df, id_vars="Nombre", value_vars=["Producción Minima Anual", "Producción Máxima Anual"])
produccion["value"] = produccion["value"]/1000
sns.barplot(data=produccion, x="Nombre", y="value", hue="variable", ax=ax3)

ax2.tick_params(axis="x", rotation=90, labelsize=10)
ax3.tick_params(axis="x", rotation=90, labelsize=10)
ax1.set_xlabel('')
ax2.set_xlabel('')
ax3.set_xlabel('')
ax1.set_xticks([])
ax1.set_ylabel('Densidad (arboles/ha)')
ax2.set_ylabel('Cantidad de Arboles')
ax3.set_ylabel('Producción (Toneladas)')
ax3.legend(title="")
ax1.text(0.01, 0.9, "A", fontsize=16, transform=ax1.transAxes)
ax2.text(0.01, 0.95, "B", fontsize=16, transform=ax2.transAxes)
ax3.text(0.01, 0.96, "C", fontsize=16, transform=ax3.transAxes)





import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec

# Cargar datos
df = pd.read_excel(r"CastanaProd.xlsx", sheet_name="AP")
d = 0.015
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)


# Crear la figura y configurar GridSpec
fig = plt.figure(figsize=(20, 8))
gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 2, 2])  # Ajusta las alturas de las filas

# Crear subplots usando gs
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[2, 0])
ax4 = fig.add_subplot(gs[3, 0])
ax5 = fig.add_subplot(gs[0:2, 1])  
ax6 = fig.add_subplot(gs[2:4, 1])  

# Plot en ax1
sns.barplot(data=df, x="Nombre", y="ArbolesporHectarea99", ax=ax1)
ax1.set_ylim(12.5, 20)
ax1.spines["bottom"].set_visible(False)
ax1.tick_params(bottom=False)
ax1.set_xticklabels([])
ax1.set_xlabel("")
ax1.plot((-d, d), (-d, d), transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((1-d, 1+d), (-d, +d), transform=ax1.transAxes, color='k', clip_on=False)
ax1.set_ylabel("")

# Plot en ax2
sns.barplot(data=df, x="Nombre", y="ArbolesporHectarea99", ax=ax2)
ax2.set_ylim(0, 1)
ax2.spines["top"].set_visible(False)
ax2.plot((-d, d), (1-d, 1+d), transform=ax2.transAxes, color='k', clip_on=False)
ax2.plot((1-d, 1+d), (1-d, 1+d), transform=ax2.transAxes, color='k', clip_on=False)
ax2.set_xticklabels([])
ax2.set_xlabel("")
ax2.set_ylabel("Densidad (arboles/ha)")
ax2.yaxis.set_label_coords(-0.07, 1.1)

# Plot en ax3
sns.barplot(data=df, x="Nombre", y="Arboles Grandes", ax=ax3, label="Arboles Grandes")
sns.barplot(data=df, x="Nombre", y="Arboles Pequeños", ax=ax3, label="Arboles Pequeños")
ax3.set_ylim(50000, 500000)
ax3.spines["bottom"].set_visible(False)
ax3.tick_params(bottom=False)
ax3.set_xticklabels([])
ax3.set_xlabel("")
ax3.set_ylabel("")
ax3.set_yticks(ax3.get_yticks()[(ax3.get_yticks()!=500000) & (ax3.get_yticks()!=0)])
kwargs.update(transform=ax3.transAxes)
ax3.plot((-d, d), (-d, d), **kwargs)
ax3.plot((1-d, 1+d), (-d, d), **kwargs)

# Plot en ax4
sns.barplot(data=df, x="Nombre", y="Arboles Grandes", ax=ax4, label="Arboles Grandes", legend=False)
sns.barplot(data=df, x="Nombre", y="Arboles Pequeños", ax=ax4, label="Arboles Pequeños", legend=False)
ax4.set_ylim([0, 40000])
ax4.spines["top"].set_visible(False)
ax4.set_xlabel("")
ax4.set_ylabel("Cantidad de Arboles")
ax4.yaxis.set_label_coords(-0.09, 1.1)
kwargs.update(transform=ax4.transAxes)
ax4.plot((-d, d), (1-d, 1+d), **kwargs)
ax4.plot((1-d, 1+d), (1-d, 1+d), **kwargs)
ax4.tick_params(axis="x", rotation=90, labelsize=10)

# Plot en ax5 (columna derecha)

produccion = pd.melt(df, id_vars="Nombre", value_vars=["Producción Minima Anual", "Producción Máxima Anual"])
produccion["value"] = produccion["value"]/1000
# Plot en ax5 (parte superior)
sns.barplot(data=produccion, x="Nombre", y="value", hue="variable", ax=ax5)
ax5.set_ylim(4000, 12000)  
ax5.spines['bottom'].set_visible(False)  
ax5.tick_params(bottom=False)  
ax5.legend(title="")
ax5.set_xticklabels([])
ax5.set_xlabel('')
ax5.set_ylabel('')

# Plot en ax6 (parte inferior)
sns.barplot(data=produccion, x="Nombre", y="value", hue="variable", ax=ax6, legend=False)
ax6.set_ylim(0, 600)  
ax6.spines['top'].set_visible(False)  
ax6.tick_params(axis="x", rotation=90, labelsize=10)
ax6.set_xlabel('') 
ax6.set_ylabel('Producción (Toneladas)')
ax6.yaxis.set_label_coords(-0.09, 1.1)
# Añadir quiebres visuales

kwargs = dict(transform=ax5.transAxes, color='k', clip_on=False)
ax5.plot((-d, +d), (-d, +d), **kwargs)  
ax5.plot((1-d, 1+d), (-d, +d), **kwargs)  

kwargs.update(transform=ax6.transAxes)  
ax6.plot((-d, +d), (1-d, 1+d), **kwargs)  
ax6.plot((1-d, 1+d), (1-d, 1+d), **kwargs)  


ax1.text(0.01, 0.7, "A", fontsize=16, transform=ax1.transAxes)
ax3.text(0.01, 0.81, "B", fontsize=16, transform=ax3.transAxes)
ax5.text(0.01, 0.81, "C", fontsize=16, transform=ax5.transAxes)
