import os
import time


def titulo(txt):
    print(f"\n=== {txt} ===")


# ---------------------------------------------------------------- NIVEL 1
# Funciones básicas con cierres

#Generador de Formateadores con Transformación
def crear_formateador(prefijo, fn_transformacion):
    def formateador(texto):
        texto_limpio = fn_transformacion(texto)
        return prefijo + texto_limpio
    return formateador

#Multiplicador Paramétrico con Mapeo
def crear_operador(factor, operacion):
    def operador(x):
        return operacion(x, factor)
    return operador

#Calculador de Descuentos con Regla Dinámica
def crear_descuento_dinamico(condicion, porcentaje=0.15):
    def descuento(precio):
        if condicion(precio):
            return round(precio * (1 - porcentaje), 2)
        return precio
    return descuento

#Generador de Seriales / Nombres Único
def crear_generador_sufijos(patron):
    contador = 0

    def generador(nombre_archivo):
        nonlocal contador
        contador += 1
        nombre, extension = os.path.splitext(nombre_archivo)
        return patron(nombre, extension, contador)
    return generador

#Conversor de Divisas con Margen
def crear_conversor(tasa, margen):
    def conversor(monto):
        base = monto * tasa
        extra = margen(base)
        return round(base + extra, 2)
    return conversor


# ---------------------------------------------------------------- NIVEL 2


#Contador Ponderado
def crear_contador_paso(fn_paso):
    cuenta = 0

    def contador():
        nonlocal cuenta
        cuenta = fn_paso(cuenta)
        return cuenta
    return contador

#Acumulador con Filtro de Aceptación
def crear_acumulador_validado(criterio):
    total = 0

    def acumulador(valor):
        nonlocal total
        if criterio(valor):
            total += valor
        return total
    return acumulador

#Promediador con Eliminación de Valores Extremos
def crear_promediador_filtrado(filtro_ruido):
    datos = []

    def promediador(valor):
        if not filtro_ruido(valor, datos):
            datos.append(valor)

        if not datos:
            return 0.0
        return sum(datos) / len(datos)
    return promediador

#Limitador de Tasa Inteligente (Rate Limiter con Reset)
def crear_limitador_avanzado(max_intentos, fn_alerta):
    intentos = 0

    def limitador():
        nonlocal intentos
        intentos += 1
        if intentos > max_intentos:
            fn_alerta(intentos)
            return False
        return True

    def reset():
        nonlocal intentos
        intentos = 0

    limitador.reset = reset
    return limitador

#Interruptor Múltiple (Máquina de Estados Ligera)
def crear_conmutador(estados):
    indice = -1

    def conmutador():
        nonlocal indice
        indice = (indice + 1) % len(estados)
        return estados[indice]
    return conmutador


# ---------------------------------------------------------------- NIVEL 3

#Pipeline de Mapeo y Filtrado Combinado
def procesar_coleccion(lista, fn_predicado, fn_transformacion):
    resultado = []
    for item in lista:
        if fn_predicado(item):
            resultado.append(fn_transformacion(item))
    return resultado

#Reductor / Agrupador Personalizado
def agrupar_por(lista, fn_clave):
    grupos = {}
    for item in lista:
        clave = fn_clave(item)
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(item)
    return grupos

#Ejecutor Repetitivo con Estado Accesible
def ejecutar_y_rastrear(fn_tarea, n):
    historial = []
    for i in range(n):
        historial.append(fn_tarea(i))

    def rastreador():
        return historial[:]
    return rastreador

#Compositor de Cadenas de Operaciones
def componer_dos(f, g):
    def funcion(x):
        return f(g(x))
    return funcion

#Decorador / HOF de Profiling y Auditoría
def auditar_ejecucion(fn_objetivo, fn_logger):
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = fn_objetivo(*args, **kwargs)
        fin = time.perf_counter()

        fn_logger({
            "funcion": fn_objetivo.__name__,
            "args": args,
            "resultado": resultado,
            "segundos": round(fin - inicio, 6),
        })
        return resultado
    return envoltura


# ---------------------------------------------------------------- NIVEL 4

#Validador Compuesto de Reglas de Negocio
def crear_validador_multiple(*lambdas_criterios):
    def validador(objeto):
        for criterio in lambdas_criterios:
            if not criterio(objeto):
                return False
        return True
    return validador


crear_validador_múltiple = crear_validador_multiple

#Caché con Expiración o Tamaño Máximo (Memoización Profesional)
def memoizar_avanzado(fn_costosa, max_items):
    cache = {}

    def memoizada(*args):
        if args in cache:
            return cache[args]

        resultado = fn_costosa(*args)
        cache[args] = resultado

        if len(cache) > max_items:
            primera_clave = next(iter(cache))
            del cache[primera_clave]

        return resultado

    memoizada.claves = lambda: list(cache.keys())
    return memoizada

#Motor de Pipeline Secuencial (Currying / Middleware)
def crear_pipeline(*funciones_transformacion):
    def pipeline(dato):
        for fn in funciones_transformacion:
            dato = fn(dato)
        return dato
    return pipeline

#Sistema Pub/Sub (Event Listener con HOFs y Closures)
def crear_sistema_eventos():
    suscriptores = {}

    def gestor(accion, evento, payload=None):
        if accion == "suscribir":
            if evento not in suscriptores:
                suscriptores[evento] = []
            suscriptores[evento].append(payload)
        elif accion == "emitir":
            resultados = []
            for fn in suscriptores.get(evento, []):
                resultados.append(fn(payload))
            return resultados
        else:
            raise ValueError("Acción inválida. Usa 'suscribir' o 'emitir'.")
    return gestor

#Mini-Query Engine sobre Listas de Objetos
def crear_consultor(campo):
    def con_condicion(fn_condicion):
        def consultar(lista):
            resultado = []
            for item in lista:
                if fn_condicion(item[campo]):
                    resultado.append(item)
            return resultado
        return consultar
    return con_condicion


# ---------------------------------------------------------------- PRUEBAS
if __name__ == "__main__":
    titulo("N1-1 Formateador")
    f = crear_formateador("Hola, ", lambda t: t.strip().title())
    print(f("  ana maría "))

    titulo("N1-2 Operador")
    print(crear_operador(3, lambda x, k: x * k)(5), crear_operador(2, lambda x, k: x ** k)(6))

    titulo("N1-3 Descuento dinámico")
    d = crear_descuento_dinamico(lambda p: p > 100, 0.2)
    print(d(150), d(80))

    titulo("N1-4 Sufijos")
    g = crear_generador_sufijos(lambda b, e, n: f"{b}_{n:03d}{e}")
    print(g("foto.jpg"), g("foto.jpg"), g("doc.pdf"))

    titulo("N1-5 Conversor")
    c = crear_conversor(0.92, lambda base: base * 0.02)
    print(c(100))

    titulo("N2-6 Contador paso")
    cp = crear_contador_paso(lambda n: n + 5 if n < 10 else n + 1)
    print([cp() for _ in range(5)])

    titulo("N2-7 Acumulador validado")
    ac = crear_acumulador_validado(lambda v: v > 10)
    print([ac(v) for v in (5, 20, 3, 15)])

    titulo("N2-8 Promediador filtrado")
    pf = crear_promediador_filtrado(
        lambda v, datos: len(datos) >= 3 and abs(v - sum(datos) / len(datos)) > 50)
    print([round(pf(v), 2) for v in (10, 12, 11, 500, 13)])

    titulo("N2-9 Limitador")
    lim = crear_limitador_avanzado(2, lambda n: print(f"  ¡ALERTA! intento {n}"))
    print([lim() for _ in range(4)])
    lim.reset()
    print("tras reset:", lim())

    titulo("N2-10 Conmutador")
    cm = crear_conmutador(["ON", "OFF", "STANDBY"])
    print([cm() for _ in range(5)])

    titulo("N3-11 Procesar colección")
    print(procesar_coleccion(range(1, 11), lambda x: x % 2 == 0, lambda x: x ** 2))

    titulo("N3-12 Agrupar por")
    personas = [{"n": "Ana", "ciudad": "Quito"}, {"n": "Luis", "ciudad": "Guayaquil"},
                {"n": "Eva", "ciudad": "Quito"}]
    print(agrupar_por(personas, lambda p: p["ciudad"]))

    titulo("N3-13 Ejecutar y rastrear")
    print(ejecutar_y_rastrear(lambda i: i ** 2, 5)())

    titulo("N3-14 Componer")
    print(componer_dos(lambda x: x + 1, lambda x: x * 2)(5))

    titulo("N3-15 Auditar")
    suma = lambda a, b: a + b
    suma.__name__ = "suma"
    print(auditar_ejecucion(suma, lambda r: print("  LOG:", r))(2, 3))

    titulo("N4-16 Validador múltiple")
    v = crear_validador_multiple(lambda u: u["edad"] >= 18, lambda u: "@" in u["email"])
    print(v({"edad": 20, "email": "a@b.com"}), v({"edad": 16, "email": "a@b.com"}))

    titulo("N4-17 Memoización con límite")
    llamadas = []

    def cuadrado(x):
        llamadas.append(x)
        return x * x

    m = memoizar_avanzado(cuadrado, 2)
    m(2)
    m(3)
    m(2)
    m(4)
    m(3)
    print("cálculos reales:", llamadas, "| caché:", m.claves())

    titulo("N4-18 Pipeline")
    p = crear_pipeline(str.strip, str.upper, lambda s: s.replace(" ", "_"))
    print(p("  hola mundo "))

    titulo("N4-19 Pub/Sub")
    ev = crear_sistema_eventos()
    ev("suscribir", "pedido", lambda d: f"Email enviado: {d}")
    ev("suscribir", "pedido", lambda d: f"Stock actualizado: {d}")
    print(ev("emitir", "pedido", "#123"))

    titulo("N4-20 Mini-query engine")
    prods = [{"nombre": "Mouse", "precio": 20}, {"nombre": "Monitor", "precio": 250},
             {"nombre": "Teclado", "precio": 45}]
    por_precio = crear_consultor("precio")
    print(por_precio(lambda p: 20 < p < 300)(prods))