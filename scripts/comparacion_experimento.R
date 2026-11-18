# comparacion_experimento.R — Comparación de grupos (R)
# Completa los pasos marcados con TODO. Ejecuta desde la raíz del repositorio:
#   Rscript scripts/comparacion_experimento.R

# ==============================================================================
# PARTE 1: PLANTILLA BASE DE REGISTRO (4 FILAS) - SECCIÓN 9 DEL PROTOCOLO
# ==============================================================================

# TODO 1: carga plantillas/registro_experimento.csv (read.csv)
df <- read.csv("plantillas/registro_experimento.csv", stringsAsFactors = FALSE)
cat("=== Vista previa de plantillas/registro_experimento.csv ===\n")
print(head(df))

# TODO 2: calcula e imprime el promedio de ventas_producto por ubicacion (aggregate)
cat("\n=== Promedio de ventas_producto por ubicacion (plantilla base) ===\n")
print(aggregate(ventas_producto ~ ubicacion, data = df, FUN = mean))

# TODO 3: imprime el número de registros por grupo (table)
cat("\n=== Número de registros por grupo (plantilla base) ===\n")
print(table(df$ubicacion))

# TODO 4: escribe 2–3 líneas de interpretación (sección 9 de la plantilla):
#         por qué con 4 filas no se puede concluir y qué le faltaría al análisis
cat("\n=== Interpretación (Sección 9) ===\n")
cat(
    "Con solo 4 filas de datos (2 observaciones por grupo), el promedio por ubicación no permite\n",
    "concluir si existe un incremento real en las ventas, debido al tamaño muestral insuficiente,\n",
    "la falta de potencia estadística y la confusión entre efectos de tienda y semana. Se requiere\n",
    "ejecutar el diseño completo (N = 40 unidades semana-tienda en 10 tiendas) y realizar un análisis\n",
    "pareado con control de covariables e intervalos de confianza.\n",
    sep = ""
)

# ==============================================================================
# PARTE 2: ANÁLISIS DEL DISEÑO SIMULADO COMPLETO (N = 40 SEMANA-TIENDA)
# ==============================================================================

ruta_sim <- "plantillas/resultado_simulacion.csv"
if (file.exists(ruta_sim)) {
    df_sim <- read.csv(ruta_sim, stringsAsFactors = FALSE)

    cat("\n=== Promedio global simulado por ubicacion (N = 40) ===\n")
    print(aggregate(ventas_producto ~ ubicacion, data = df_sim, FUN = mean))

    media_tienda <- tapply(df_sim$ventas_producto, list(df_sim$tienda, df_sim$ubicacion), mean)
    diferencias <- media_tienda[, "pasillo_principal"] - media_tienda[, "habitual"]

    tabla_pareada <- cbind(round(media_tienda, 2), diferencia = round(diferencias, 2))
    cat("\n=== Análisis pareado por tienda ===\n")
    print(tabla_pareada)

    cat(sprintf("\nPromedio de la diferencia pareada: %.2f unidades/semana\n", mean(diferencias)))
    cat(sprintf("Desviación estándar de la diferencia: %.2f unidades/semana\n", sd(diferencias)))
} else {
    cat("\nNota: Ejecute primero 'python scripts/comparacion_experimento.py' para generar plantillas/resultado_simulacion.csv\n")
}
