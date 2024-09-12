import requests
import tkinter as tk
from tkinter import ttk

class Datos_Trans:
    @staticmethod
    def convierte_a_numero(dato, numeri_column):
        for item in dato:
            for column in numeri_column:
                try:
                    item[column] = int(item[column])
                except (ValueError, KeyError):
                    pass
        return dato

class RecuperadorDatos:
    def __init__(self, url_api):
        self.url_api = url_api
        self.dataset = []

    def obtener_datos(self):
        respuesta = requests.get(self.url_api)
        if respuesta.status_code == 200:
            self.dataset = respuesta.json()
            numeri_columns = ['id']
            self.dataset = Datos_Trans.convierte_a_numero(self.dataset, numeri_columns)
        else:
            print("Error al obtener datos de la API")

    def obtener_dataset(self):
        return self.dataset

class ProcesadorDatos:
    def __init__(self, dataset):
        self.dataset = dataset

    def ordenar_por_variable(self, variable, algoritmo):
        if algoritmo == "QuickSort":
            self.dataset = self.quick_sort(self.dataset, variable)
        elif algoritmo == "MergeSort":
            self.dataset = self.merge_sort(self.dataset, variable)
        elif algoritmo == "BubbleSort":
            self.dataset = self.bubble_sort(self.dataset, variable)
        else:
            print("Algoritmo no soportado")

    def quick_sort(self, datos, variable):
        if len(datos) <= 1:
            return datos
        pivote = datos[len(datos) // 2].get(variable, 0)
        izquierda = [x for x in datos if x.get(variable, 0) < pivote]
        medio = [x for x in datos if x.get(variable, 0) == pivote]
        derecha = [x for x in datos if x.get(variable, 0) > pivote]
        return self.quick_sort(izquierda, variable) + medio + self.quick_sort(derecha, variable)

    def merge_sort(self, datos, variable):
        if len(datos) > 1:
            medio = len(datos) // 2
            mitad_izquierda = datos[:medio]
            mitad_derecha = datos[medio:]
            self.merge_sort(mitad_izquierda, variable)
            self.merge_sort(mitad_derecha, variable)
            i = j = k = 0
            while i < len(mitad_izquierda) and j < len(mitad_derecha):
                if mitad_izquierda[i].get(variable, 0) < mitad_derecha[j].get(variable, 0):
                    datos[k] = mitad_izquierda[i]
                    i += 1
                else:
                    datos[k] = mitad_derecha[j]
                    j += 1
                k += 1
            while i < len(mitad_izquierda):
                datos[k] = mitad_izquierda[i]
                i += 1
                k += 1
            while j < len(mitad_derecha):
                datos[k] = mitad_derecha[j]
                j += 1
                k += 1
        return datos

    def bubble_sort(self, datos, variable):
        n = len(datos)
        for i in range(n):
            for j in range(0, n-i-1):
                if datos[j].get(variable, 0) > datos[j+1].get(variable, 0):
                    datos[j], datos[j+1] = datos[j+1], datos[j]
        return datos

class Aplicacion:
    def __init__(self, url_api):
        self.recuperador_datos = RecuperadorDatos(url_api)
        self.dataset = []
        self.procesador_datos = None

    def ejecutar(self):
        self.recuperador_datos.obtener_datos()
        self.dataset = self.recuperador_datos.obtener_dataset()
        self.procesador_datos = ProcesadorDatos(self.dataset)

class AplicacionGUI:
    def __init__(self, root, procesador_datos):
        self.procesador_datos = procesador_datos
        self.root = root
        self.root.geometry("1000x700")
        self.root.title("Trabajo de Pool - 15%")
        self.root.configure(bg="#e6e6fa")
        self.crear_widgets()

    def crear_widgets(self):
        self.titulo = tk.Label(self.root, text="Trabajo de Pooll - 15%", font=("Comic Sans MS", 20, "bold"), bg="#e6e6fa", fg="#4682b4")
        self.titulo.pack(pady=20)

        frame_controles = tk.Frame(self.root, bg="#e6e6fa")
        frame_controles.pack(pady=20, padx=20, fill=tk.X)

        self.etiqueta_variable = tk.Label(frame_controles, text="Variable:", font=("Arial", 12, "bold"), bg="#e6e6fa", fg="#333333")
        self.etiqueta_variable.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.combobox_variable = ttk.Combobox(frame_controles, values=["id", "name", "username", "email"], font=("Arial", 12))
        self.combobox_variable.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.etiqueta_algoritmo = tk.Label(frame_controles, text="Algoritmo:", font=("Arial", 12, "bold"), bg="#e6e6fa", fg="#333333")
        self.etiqueta_algoritmo.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.combobox_algoritmo = ttk.Combobox(frame_controles, values=["QuickSort", "MergeSort", "BubbleSort"], font=("Arial", 12))
        self.combobox_algoritmo.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.boton_ordenar = tk.Button(frame_controles, text="Ordenar", command=self.ordenar_datos, font=("Arial", 12, "bold"), bg="#32cd32", fg="white", relief=tk.RAISED)
        self.boton_ordenar.grid(row=2, column=0, columnspan=2, pady=20)

        self.frame_resultado = tk.Frame(self.root, bg="#e6e6fa")
        self.frame_resultado.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.frame_resultado, columns=("ID", "Name", "Username", "Email"), show='headings', height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Email", text="Email")
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#87ceeb", foreground="black")
        style.configure("Treeview", font=("Arial", 11), background="#ffffff", foreground="black")
        
        self.tree.pack(fill=tk.BOTH, expand=True)

    def ordenar_datos(self):
        variable = self.combobox_variable.get()
        algoritmo = self.combobox_algoritmo.get()
        if variable and algoritmo:
            self.procesador_datos.ordenar_por_variable(variable, algoritmo)
            self.mostrar_datos()
        else:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", tk.END, values=("Por favor, seleccione una variable y un algoritmo.", "", "", ""))

    def mostrar_datos(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.procesador_datos.dataset:
            self.tree.insert("", tk.END, values=(
                item.get("id", ""),
                item.get("name", ""),
                item.get("username", ""),
                item.get("email", "")
            ))

if __name__ == "__main__":
    URL_API = "https://jsonplaceholder.typicode.com/users"
    app = Aplicacion(URL_API)
    app.ejecutar()
    root = tk.Tk()
    app_gui = AplicacionGUI(root, app.procesador_datos)
    root.mainloop()
