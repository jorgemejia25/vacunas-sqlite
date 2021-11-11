import hashlib
import sqlite3


contrasenaEncriptada = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"

con = sqlite3.connect('vacunas.db')
cur = con.cursor()

bucle = True

cur.execute('''CREATE TABLE IF NOT EXISTS "puestos" (
	"ubicacion"	TEXT NOT NULL,
	"vacunas"	TEXT NOT NULL,
	"puestos cercanos"	TEXT NOT NULL,
	"tiempo aproximado"	TEXT NOT NULL
    );''')

con.commit()


def menuNormal():
    """Este menú busca el puesto de vacunación con menor tiempo de espera y con la vacuna requerida."""
    try:
        opcion = int(input('''Por favor, seleccione una opcion: \n
            1. Ver el puesto de vacunación recomendado.
            2. Salir. \n'''))

        if (opcion == 1):
            puestos = cur.execute('SELECT * FROM puestos').fetchall()

            tiempoArray = []

            vacuna = input("Ingrese la vacuna que desea: ")

            puestosRecomendados = []
            for row in puestos:
                if(vacuna.upper() in row[1].upper()):
                    tiempoArray.append(int(row[-1]))
                    puestosRecomendados.append(row)

            if(len(puestosRecomendados) > 0):
                index = 0
                for puesto in puestosRecomendados:
                    if(int(puesto[-1]) == min(tiempoArray)):
                        print("\nPuesto con menor tiempo y con esa vacuna: ")
                        print(f"Ubicación: {puesto[0]}")
                        print(f"Tiempo de espera aproximado: {puesto[-1]}\n")
                        puestosRecomendados.pop(index)
                    index += 1

                if(len(puestosRecomendados) > 0):
                    print("Otros puestos con esa vacuna:")
                    for puesto in puestosRecomendados:
                        print(f"\nUbicación: {puesto[0]}")
                        print(f"Tiempo de espera aproximado: {puesto[-1]}\n")
            else:
                print("No se encontró ningún puesto con esa vacuna.")

        else:
            menuPrincipal()
    except:
        print("Error.")


def menuAdministrador():
    """
    Menú de administrador, utiliza autenticación encriptada y permite ingresar, editar, 
    ver o eliminar puestos de vacunación.
    """
    contrasenaSinEncriptar = input("Por favor ingrese la contraseña: ")

    # Encriptamos la contraseña con sha-256 para una seguridad mas alta.
    # Contraseña original: 123456

    contrasena = hashlib.sha256(
        contrasenaSinEncriptar.encode('utf-8')).hexdigest()

    if(contrasena == contrasenaEncriptada):
        print("Bienvenido")

        opcion = int(input('''Por favor, seleccione una opcion: \n
            1. Ver todos los puestos de vacunación.
            2. Agregar un nuevo puesto de vacunación.
            3. Editar un puesto de vacunación. 
            4. Eliminar un puesto de vacunación. 
            5. Salir. \n'''))

        if (opcion == 1):
            todosLosPuestos()
        elif(opcion == 2):
            menuAgregar()
        elif(opcion == 3):
            menuEditar()
        elif(opcion == 4):
            menuEliminar()
        else:
            menuPrincipal()
    else:
        print("La contraseña no es válida.")
        menuPrincipal()


def todosLosPuestos():
    """Muestra todos los puestos con un bucle for."""

    print("Estos son todos los puestos")

    for row in cur.execute('SELECT * FROM puestos'):
        print(f'\nUbicación: {row[0]}')
        print(f'Vacunas: {row[1]}')
        print(f'Puestos cercanos: {row[2]}')
        print(f'Tiempo estimado: {row[3]}\n')


def menuAgregar():
    """Agrega un nuevo puesto"""

    print("Por favor, llene los siguientes datos.")
    ubicacion = input("Ingrese la ubicacion del puesto de vacunación: ")
    vacunas = input("Ingrese las vacunas disponibles (Separelos por coma): ")
    puestos_cercanos = input(
        "Ingrese los puestos cercanos (Separelos por coma): ")
    tiempo_estimado = input("Ingrese el tiempo estimado en minutos: ")

    cur.execute("insert into puestos values (?, ?, ?, ?)",
                (ubicacion, vacunas, puestos_cercanos, tiempo_estimado))

    con.commit()

    print("Puesto agregado.")


def menuEditar():
    """Edita el puesto seleccionado"""
    try:
        index = 1
        print("Seleccione la ubicacion del puesto a editar.\n")

        puestos = cur.execute('SELECT "ubicacion" FROM puestos').fetchall()

        for row in puestos:
            print(f'{index}. Puesto de vacunacion: {row[0]}')
            index += 1

        puesto = int(input("Ingrese el número de puesto: "))

        print('\nEditar puesto de vacunación.\n')

        print('1. Editar ubicación')
        print('2. Editar vacunas disponibles')
        print('3. Editar puestos cercanos')
        print('4. Editar tiempo aproximado')

        opcion = int(input('\nSeleccione la opción: '))

        nuevo_campo = input('Inserte el nuevo contenido del campo: \n')

        if(opcion == 1):
            cur.execute(
                f'UPDATE puestos SET "ubicacion" = "{nuevo_campo}" WHERE ubicacion = "{puestos[puesto - 1][0]}"')
            con.commit()

        elif(opcion == 2):
            cur.execute(
                f'UPDATE puestos SET "vacunas" = "{nuevo_campo}" WHERE ubicacion = "{puestos[puesto - 1][0]}"')
            con.commit()

        elif(opcion == 3):
            cur.execute(
                f'UPDATE puestos SET "puestos cercanos" = "{nuevo_campo}" WHERE ubicacion = "{puestos[puesto - 1][0]}"')
            con.commit()

        elif(opcion == 4):
            cur.execute(
                f'UPDATE puestos SET "tiempo aproximado" = "{nuevo_campo}" WHERE ubicacion = "{puestos[puesto - 1][0]}"')
            con.commit()

        print("Puesto actualizado con éxito.")
    except:
        print("Error. Puede que haya sido causado por haber seleccionado un puesto o una opción inválida.")


def menuEliminar():
    """Elimina el puesto seleccionado"""
    try:
        index = 1
        print("Seleccione la ubicacion del puesto a eliminar.\n")

        puestos = cur.execute('SELECT "ubicacion" FROM puestos').fetchall()

        for row in puestos:
            print(f'{index}. Puesto de vacunacion: {row[0]}')
            index += 1

        puesto = int(input("Ingrese el número de puesto: "))

        cur.execute(
            f'DELETE FROM puestos WHERE ubicacion = "{puestos[puesto - 1][0]}"')
        con.commit()
    except:
        print("Error. Puede que haya sido causado por haber seleccionado un puesto o una opción inválida.")


while (True):
    """Menú principal. Permite seleccionar entre el menú de administrador o el menú por defecto."""

    print("\nBienvenido a la aplicacion de puestos de vacunación. ")
    opcion = int(input('''Por favor, seleccione una opción: \n
        1. Buscar puesto de vacunación. 
        2. Registrar/Actualizar puesto de vacunación (Administrador). 
        3. Salir \n'''))

    if(opcion == 1):
        menuNormal()
    elif(opcion == 2):
        menuAdministrador()
    else:
        break

con.close()
