# comparacion_experimento.py — Comparación de grupos (Python)
# Completa los pasos marcados con TODO. Ejecuta desde la raíz del repositorio:
#   python scripts/comparacion_experimento.py

import pandas as pd
import numpy as np

# ==============================================================================
# PARTE 1: PLANTILLA BASE DE REGISTRO (4 FILAS) - SECCIÓN 9 DEL PROTOCOLO
# ==============================================================================

# TODO 1: carga plantillas/registro_experimento.csv con pandas
df = pd.read_csv("plantillas/registro_experimento.csv")
print("=== Vista previa de plantillas/registro_experimento.csv ===")
print(df.head())

# TODO 2: calcula e imprime el promedio de ventas_producto por ubicacion
print("\n=== Promedio de ventas_producto por ubicacion (plantilla base) ===")
print(df.groupby("ubicacion")["ventas_producto"].mean())

# TODO 3: imprime el número de registros por grupo (value_counts)
print("\n=== Número de registros por grupo (plantilla base) ===")
print(df["ubicacion"].value_counts())

# TODO 4: escribe 2–3 líneas de interpretación (sección 9 de la plantilla):
#         por qué con 4 filas no se puede concluir y qué le faltaría al análisis
print("\n=== Interpretación (Sección 9) ===")
print(
    "Con solo 4 filas de datos (2 observaciones por grupo), el promedio por ubicación es meramente "
    "ilustrativo y no permite concluir si existe un efecto causal real, ya que la muestra carece de "
    "potencia estadística y confunde la variabilidad propia entre tiendas y semanas con el efecto del "
    "tratamiento. Para validar la hipótesis se requiere ejecutar el protocolo completo (N = 40 unidades "
    "semana-tienda en 10 sucursales), controlar factores externos y aplicar inferencia estadística pareada."
)

# ==============================================================================
# PARTE 2: DISEÑO CRUZADO ALEATORIZADO Y SIMULACIÓN (N = 40 SEMANA-TIENDA)
# ==============================================================================

tiendas = [
    "Quito Norte", "Quito Sur", "Guayaquil Centro", "Guayaquil Norte",
    "Cuenca Centro", "Cuenca Sur", "Ambato Centro", "Manta", "Loja", "Machala"
]
semanas = [1, 2, 3, 4]

# Sorteo de la condición inicial (Aleatorización con semilla fija)
rng = np.random.default_rng(1234597)  # Semilla para reproducibilidad de la asignación
primera = rng.choice(["pasillo_principal", "habitual"], size=len(tiendas))

filas = []
for tienda, cond in zip(tiendas, primera):
    otra = "habitual" if cond == "pasillo_principal" else "pasillo_principal"
    for s in semanas:
        filas.append({
            "tienda": tienda,
            "semana": s,
            "ubicacion": cond if s % 2 == 1 else otra
        })

diseno = pd.DataFrame(filas)

# Simulación de la ejecución experimental (4 semanas x 10 tiendas = 40 unidades)
rng_sim = np.random.default_rng(1234598)  # Semilla para reproducibilidad de simulación
efecto_tienda = dict(zip(tiendas, rng_sim.normal(1100, 120, len(tiendas))))
efecto_semana = {1: 0, 2: 30, 3: 60, 4: 90}

diseno["ventas_producto"] = (
    diseno["tienda"].map(efecto_tienda) +
    diseno["semana"].map(efecto_semana) +
    (diseno["ubicacion"] == "pasillo_principal") * 220 +
    rng_sim.normal(0, 90, len(diseno))
).round(0).astype(int)

# Registro de evento confusor controlado: promoción simultánea
diseno["promocion_simultanea"] = "no"
diseno.loc[(diseno["tienda"] == "Guayaquil Centro") & (diseno["semana"] == 1), "promocion_simultanea"] = "si"
diseno.loc[diseno["promocion_simultanea"] == "si", "ventas_producto"] += 180

# Guardar resultado de la simulación
diseno.to_csv("plantillas/resultado_simulacion.csv", index=False)

# Análisis pareado: una fila por tienda con sus condiciones promedio
piv = diseno.groupby(["tienda", "ubicacion"])["ventas_producto"].mean().unstack()
piv["diferencia"] = piv["pasillo_principal"] - piv["habitual"]

media = piv["diferencia"].mean()
dev = piv["diferencia"].std(ddof=1)

print("\n=== Resultados del Diseño Experimental Completo (N = 40 unidades semana-tienda) ===")
print(piv.round(2))
print(f"\nPromedio de la diferencia de ventas entre ubicaciones: {media:.2f} unidades/semana")
print(f"Desviación estándar de la diferencia de ventas entre ubicaciones: {dev:.2f} unidades/semana")