#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#       Proyecto POO
#////////////////////////////////////////////////////////////////////

# Las vacunas fueron extraídas de:
# Perros --> http://www.mundoanimalia.com/articulo/Vacunas_para_perros
# Gatos  --> http://www.guioteca.com/mascotas/vacunas-para-gatos-cuales-son-y-cuando-ponerlas/
# Hamster -> No existen vacunas para hamsters
# Aves   --> https://www.hipra.com/wps/portal/web/inicio/nuestrosProductos/!ut/p/c4/04_SB8K8x
#            LLM9MSSzPy8xBz9CP0os3gDU8dASydDRwMLpwADA09PC2cXA3MnAwtDM_2CbEdFAC9kTgw!/?WCM_GLO
#            BAL_CONTEXT=/productos_es/hipra/secciones/nuestrosproductos/00/127555/119923_00/
#            127517_00&PageDesign=web_recursos/PPNuestrosProductosSeccion2
# Conejo --> http://www.madrigueraweb.org/articulo/vacunas-proteger-a-nuestros-conejos

c = 0

class Cliente():
    def __init__(self, codigo, nombre, apellido, sexo, edad):
        self.id = codigo
        self.nombre = nombre
        self.apellido = apellido
        self.sexo = sexo
        self.edad = edad
    def cantidadMascotas(self):
        cantidad = 0
        lineas = open("mascotas.txt","r").readlines()
        for linea in lineas:
            due_id = linea.strip("\n").split(",")[-1]
            if due_id == self.id:
                cantidad += 1
        return cantidad

class Mascota():
    def __init__(self, codigo, nombre, especie, raza, sexo, edad, dueño):
        self.id = codigo
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.sexo = sexo
        self.edad = edad
        self.dueño = dueño
    def agregarVacuna(self, vacuna, fecha):
        vacunas = open("vacunas.txt","r").readlines()
        especieIncluida = False
        for linea in vacunas:
            linea = linea.strip("\n").split(",")
            especie = linea[0]
            if especie == self.especie:
                especieIncluida = True; break
        if especieIncluida:
            compatible = False
            for linea in vacunas:
                linea = vacunas.strip("\n").split(",")
                especie = linea[0]; vacunaR = linea[1]
                if vacuna == vacunaR and self.especie == especie:
                    compatible = True; break
            if compatible:
                fecha += "\n"
                open("mascota_vacuna.txt","a").write(self.id+","+vacuna+","+fecha)
                open("visitas.txt","a").write(self.id+",Vacuna,"+fecha)
            else: mostrar("La vacuna no existe o pertenece a otra especie")
        else: mostrar("Las vacunas para esta especie aun no estàn disponibles")
    def agregarBaño(self,fecha):
        open("mascota_baño.txt","a").write(self.id+","+fecha+"\n")
        open("visitas.txt","a").write(self.id+",Baño,"+fecha+"\n")
    def agregarCorte(self,fecha):
        open("mascota_corte.txt","a").write(self.id+","+fecha+"\n")
        open("visitas.txt","a").write(self.id+",Corte,"+fecha+"\n")
    def agregarAtencionMedica(self,atencion,fecha):
        open("mascota_atencion.txt","a").write(self.id+","+atencion+","+fecha)
        open("visitas.txt","a").write(self.id+",Atencion Medica,"+fecha+"\n")
    def vecesEnArchivo(self,archivo):
        cantidad = 0
        lineas = open(archivo,"r").readlines()
        for linea in lineas:
            linea = linea.strip("\n").split(",")
            if linea[0] == self.id:
                cantidad += 1
        return cantidad
    def listaVisitas(self):
        lista = []
        lineas = open("visitas.txt","r").readlines()
        for linea in lineas:
            linea = linea.strip("\n").split(",")
            if self.id == linea[0]:
                lista.append(linea)
        lista.sort(key=lambda i:i[2])
        return lista
    def numeroVisitas(self):
        visitas = 0
        visitas += self.vecesEnArchivo("mascota_vacuna.txt")
        visitas += self.vecesEnArchivo("mascota_baño.txt")
        visitas += self.vecesEnArchivo("mascota_corte.txt")
        visitas += self.vecesEnArchivo("mascota_atencion.txt")
        return visitas

# Codigo principal

from tkinter import *

class Ingreso(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Control de ingreso a Earl's PetShop BD")
        self.resizable(0,0)
        self.config(bg="#eee")
        self.geometry("370x230")
        self.enter1, self.enter2 = StringVar(),StringVar()
        
        fgLbl = "#000"; ftLbl = ("Calibri",12); ftTit = ("Calibri",20)
        Label(text="Usuario:",fg=fgLbl,font=ftLbl).place(x=70,y=80)
        Label(text="Contraseña:",fg=fgLbl,font=ftLbl).place(x=70,y=120)
        Label(text="Bienvenido a Earl's PetShop",font=ftTit).place(x=30,y=20)
        
        self.entNombre = Entry(self,textvariable=self.enter1,\
            highlightcolor="#f00",highlightthickness="1")
        self.entNombre.place(x=170,y=83)
        self.entContra = Entry(self,textvariable=self.enter2,show="*",\
            highlightcolor="#f00",highlightthickness="1")
        self.entContra.place(x=170,y=123)
        
        self.entNombre.bind("<Return>",self.iniciarSes)
        self.entContra.bind("<Return>",self.iniciarSes)

        ftBtn = ("Calibri",12);
        inicio = Button(self, text="Ingresar", bg="#090",fg="#fff",\
            width="10",command=self.iniciarSes)
        inicio.place(x=90, y=165)
        salir = Button(self, text="Salir", bg="#900", fg="#fff",\
            width="10", command=self.destroy)
        salir.place(x=190, y=165)
        self.mainloop()
        
    def iniciarSes(self, event=""):
        global c
        def existe(a,b): return a==b and a!=""
        users = open("usuarios.txt", "r")
        malIngreso = True
        for linea in users:
            linea = linea.strip("\n").split(",")
            user = self.enter1.get(); cont = self.enter2.get()
            if len(linea)==2 and existe(user,linea[0]) and existe(cont,linea[1]):
                self.withdraw(); Menu()
                malIngreso = False; break
        if malIngreso:
            c+=1
            if(c<3): mostrar("Inicio de sesion incorrecto")
            else: self.destroy()
        
class Menu(Tk):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Menu Principal")
        self.resizable(0,0)
        self.config(bg="#fff")
        self.geometry ("365x245")
        self.cli = StringVar()

        ftLbl = ("Calibri",12); ftTit = ("Calibri",20); n = "#000"; b = "#fff"
        Label(self,text="Menu Principal",bg=b,fg=n,font=ftTit).place(x=30,y=15)
        Label(self,text="-"*60,bg=b,fg=n,font=ftLbl).place(x=30,y=56)
        Label(self,text="Indexar Cliente",bg=b,fg=n,font=ftLbl).place(x=60,y=90)
        Label(self,text="Acceder Cliente (id)",bg=b,fg=n,font=ftLbl).place(x=60,y=125)
        Label(self,text="Mostrar Clientes",bg=b,fg=n,font=ftLbl).place(x=60,y=160)
        Label(self,text="Mostrar Mascotas",bg=b,fg=n,font=ftLbl).place(x=60,y=195)

        self.entCodCli = Entry(self,textvariable=self.cli,highlightcolor="#009",\
            highlightthickness="1", width="8", font=ftLbl)
        self.entCodCli.place(x=230,y=125)

        def indexar(): self.destroy(); Indexar()
        def acceder():
            lineas = open("clientes.txt","r").readlines()
            existe = False; lineaSelec = 0
            for linea in lineas:
                linea = linea.strip("\n").split(",")
                if linea[0] == self.cli.get():
                    lineaSelec = linea
                    existe = True; break;
            if existe:
                cliente = Cliente(linea[0],linea[1],linea[2],linea[3],linea[4])
                self.destroy(); VentanaCli(cliente)
            else: mostrar("Codigo no vàlido")
        def mostrarCli():self.destroy(); MostrarCli()
        def mostrarMas():self.destroy(); MostrarMas()

        btn1 = Button(self,text="Indexar",command=lambda: indexar(), width="12")
        btn1.place(x=230,y=90)
        btn2 = Button(self,text="⚲",command=lambda: acceder())
        btn2.place(x=306,y=125)
        btn3 = Button(self,text="Mostrar",command=lambda: mostrarCli(), width="12")
        btn3.place(x=230,y=160)
        btn4 = Button(self,text="Mostrar",command=lambda: mostrarMas(), width="12")
        btn4.place(x=230,y=195)

        self.mainloop()

class Indexar(Tk):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Agregar Cliente")
        self.resizable(0,0)
        self.config(bg="#fff")
        self.geometry("350x340")

        ftLbl = ("Calibri",12); ftTit = ("Calibri",20); n = "#000"; b = "#fff"
        Label(self,text="Agregar Cliente",bg=b,fg=n,font=ftTit).place(x=30,y=15)
        Label(self,text="-"*55,bg=b,fg=n,font=ftLbl).place(x=30,y=56)
        Label(self,text="Codigo:",bg=b,fg=n,font=ftLbl).place(x=50,y=90)
        Label(self,text="Nombre:",bg=b,fg=n,font=ftLbl).place(x=50,y=125)
        Label(self,text="Apellido:",bg=b,fg=n,font=ftLbl).place(x=50,y=160)
        Label(self,text="Sexo (m/f):",bg=b,fg=n,font=ftLbl).place(x=50,y=195)
        Label(self,text="Edad:",bg=b,fg=n,font=ftLbl).place(x=50,y=230)

        self.codigo = nuevoCodigo("clientes.txt")
        Label(self,text=self.codigo,bg=b,fg=n,font=ftLbl).place(x=170,y=90)

        self.n = StringVar(); self.a = StringVar()
        self.s = StringVar(); self.e = StringVar()
        self.nm = Entry(self,textvariable=self.n,highlightcolor="#090",\
            highlightthickness="1"); self.nm.place(x=170,y=125)
        self.ap = Entry(self,textvariable=self.a,highlightcolor="#090",\
            highlightthickness="1"); self.ap.place(x=170,y=160)
        self.sx = Entry(self,textvariable=self.s,highlightcolor="#090",\
            highlightthickness="1"); self.sx.place(x=170,y=195)
        self.ed = Entry(self,textvariable=self.e,highlightcolor="#090",\
            highlightthickness="1"); self.ed.place(x=170,y=230)

        indexar = Button(self,text="Indexar",bg="#090",fg="#fff",\
            width="10",command=self.indexar); indexar.place(x=63,y=280)
        limpiar = Button(self,text="Limpiar Campos",bg="#009",fg="#fff",\
            width="15",command=self.limpiar); limpiar.place(x=163,y=280)
        atras = Button(self, text="Atras", bg="#900", fg="#fff",\
            width="7", command=self.atras); atras.place(x=252, y=22)

    def atras(self):   self.destroy(); Menu()
    def limpiar(self): self.n.set("");self.a.set("");self.s.set("");self.e.set("")
    def indexar(self):
        def equal(n,a,s,e):
            return self.n.get()==n and self.a.get()==a and\
                   self.s.get()==s and self.e.get()==e
        def write():
            return self.n.get()+","+self.a.get()+","+\
                   self.s.get()+","+self.e.get()+"\n"
        if not esNumero(self.e.get()) or int(self.e.get())<=0:
            self.limpiar(); mostrar("Ingreso de edad incorrecto")
        elif not self.s.get() in "mf":
            self.limpiar(); mostrar("Sexo incorrecto")
        else:
            existe=False; lineas = open("clientes.txt","r").readlines()
            for linea in lineas:
                linea = linea.strip("\n").split(",")
                if equal(linea[1],linea[2],linea[3],linea[4]):
                    existe = True; break
            if not existe:
                open("clientes.txt","a").write(self.codigo+","+write())
                self.limpiar()
                mostrar("Indexaciòn exitosa")
            else:
                self.limpiar()
                mostrar("Este cliente ya existe")

class VentanaCli(Tk):
    def __init__(self,cliente):
        Toplevel.__init__(self)
        self.title("Cliente: "+cliente.id)
        self.resizable(0,0)
        self.config(bg="#fff")
        self.geometry("300x390")
        self.mas = StringVar()

        ftLbl = ("Calibri",12); ftTit = ("Calibri",20); n = "#000"; b = "#fff"
        Label(self,text="Cliente",bg=b,fg=n,font=ftTit).place(x=30,y=15)
        Label(self,text="-"*46,bg=b,fg=n,font=ftLbl).place(x=30,y=56)
        Label(self,text="Codigo:",bg=b,fg=n,font=ftLbl).place(x=50,y=90)
        Label(self,text="Nombre:",bg=b,fg=n,font=ftLbl).place(x=50,y=115)
        Label(self,text="Apellido:",bg=b,fg=n,font=ftLbl).place(x=50,y=140)
        Label(self,text="Sexo:",bg=b,fg=n,font=ftLbl).place(x=50,y=165)
        Label(self,text="Edad:",bg=b,fg=n,font=ftLbl).place(x=50,y=190)
        Label(self,text="Mascotas:",bg=b,fg=n,font=ftLbl).place(x=50,y=215)

        cantMascotas = cliente.cantidadMascotas()
        Label(self,text=cliente.id,bg=b,fg=n,font=ftLbl).place(x=160,y=90)
        Label(self,text=cliente.nombre,bg=b,fg=n,font=ftLbl).place(x=160,y=115)
        Label(self,text=cliente.apellido,bg=b,fg=n,font=ftLbl).place(x=160,y=140)
        Label(self,text=cliente.sexo,bg=b,fg=n,font=ftLbl).place(x=160,y=165)
        Label(self,text=cliente.edad,bg=b,fg=n,font=ftLbl).place(x=160,y=190)
        Label(self,text=cantMascotas,bg=b,fg=n,font=ftLbl).place(x=160,y=215)

        def atras(): self.destroy(); Menu()
        def agregar(): self.destroy(); AgregarMas(cliente)
        def acceder():
            lineas = open("mascotas.txt","r").readlines()
            existe = False; lineaSelec = 0
            for lin in lineas:
                lin = lin.strip("\n").split(",")
                if lin[1] == self.mas.get() and lin[6] == cliente.id:
                    lS = lin
                    existe = True; break;
            if existe:
                mascota = Mascota(lS[0],lS[1],lS[2],lS[3],lS[4],lS[5],lS[6])
                self.destroy(); VentanaMas(cliente,mascota)
            else: mostrar(self.mas.get()+" no es mascota de "+cliente.nombre)

        lblAcc = "Acceder mascota (nombre)"
        Label(self,text=lblAcc,bg=b,fg=n,font=ftLbl).place(x=50,y=300)
        self.nomMas = Entry(self,textvariable=self.mas,highlightcolor="#009",\
            highlightthickness="1", width="21",font=ftLbl)
        self.nomMas.place(x=50,y=330)
        acces = Button(self, text="⚲", command=acceder)
        acces.place(x=230, y=330)

        atras = Button(self, text="Atras", bg="#900", fg="#fff",\
            width="7", command=atras); atras.place(x=205, y=22)
        agreg = Button(self, text="Agregar mascota",width="27",\
            command=agregar); agreg.place(x=49, y=260)

class AgregarMas(Tk):
    def __init__(self, dueño):
        Toplevel.__init__(self)
        self.title("Nueva Mascota")
        self.resizable(0,0)
        self.config(bg="#fff")
        self.geometry("350x410")
        self.dueño = dueño

        ftLbl = ("Calibri",12); ftTit = ("Calibri",20); n = "#000"; b = "#fff"
        Label(self,text="Agregar Mascota",bg=b,fg=n,font=ftTit).place(x=30,y=15)
        Label(self,text="-"*55,bg=b,fg=n,font=ftLbl).place(x=30,y=56)
        Label(self,text="Codigo:",bg=b,fg=n,font=ftLbl).place(x=50,y=90)
        Label(self,text="Nombre:",bg=b,fg=n,font=ftLbl).place(x=50,y=125)
        Label(self,text="Especie:",bg=b,fg=n,font=ftLbl).place(x=50,y=160)
        Label(self,text="Raza:",bg=b,fg=n,font=ftLbl).place(x=50,y=195)
        Label(self,text="Sexo (m/f):",bg=b,fg=n,font=ftLbl).place(x=50,y=230)
        Label(self,text="Edad:",bg=b,fg=n,font=ftLbl).place(x=50,y=265)
        Label(self,text="Dueño:",bg=b,fg=n,font=ftLbl).place(x=50,y=300)

        self.codigo = nuevoCodigo("mascotas.txt")
        Label(self,text=self.codigo,bg=b,fg=n,font=ftLbl).place(x=170,y=90)

        self.dueño_id = dueño.id
        Label(self,text=self.dueño_id,bg=b,fg=n,font=ftLbl).place(x=170,y=300)

        self.n = StringVar(); self.es = StringVar(); self.r = StringVar()
        self.s = StringVar(); self.ed = StringVar()
        self.nm = Entry(self,textvariable=self.n,highlightcolor="#090",\
            highlightthickness="1"); self.nm.place(x=170,y=125)
        self.esp = Entry(self,textvariable=self.es,highlightcolor="#090",\
            highlightthickness="1"); self.esp.place(x=170,y=160)
        self.ra = Entry(self,textvariable=self.r,highlightcolor="#090",\
            highlightthickness="1"); self.ra.place(x=170,y=195)
        self.sx = Entry(self,textvariable=self.s,highlightcolor="#090",\
            highlightthickness="1"); self.sx.place(x=170,y=230)
        self.eda = Entry(self,textvariable=self.ed,highlightcolor="#090",\
            highlightthickness="1"); self.eda.place(x=170,y=265)

        agregar = Button(self,text="Agregar",bg="#090",fg="#fff",\
            width="10",command=self.agregar); agregar.place(x=63,y=350)
        limpiar = Button(self,text="Limpiar Campos",bg="#009",fg="#fff",\
            width="15",command=self.limpiar); limpiar.place(x=163,y=350)
        atras = Button(self, text="Atras", bg="#900", fg="#fff",\
            width="7", command=self.atras); atras.place(x=252, y=22)

    def atras(self):   self.destroy(); VentanaCli(self.dueño)
    def limpiar(self):
        self.n.set("");self.es.set("");self.r.set("");self.s.set("");self.ed.set("")
    def agregar(self):
        def equal(n,es,r,s,ed):
            return self.n.get()==n and self.es.get()==es and self.r.get()==r and\
                   self.s.get()==s and self.ed.get()==ed
        def write():
            return self.n.get()+","+self.es.get()+","+self.r.get()+","+\
                   self.s.get()+","+self.ed.get()+","+self.dueño_id+"\n"
        if not esNumero(self.ed.get()) or int(self.ed.get())<=0:
            self.limpiar(); mostrar("Ingreso de edad incorrecto")
        elif not self.s.get() in "mf":
            self.limpiar(); mostrar("Sexo incorrecto")
        else:
            open("mascotas.txt","a").write(self.codigo+","+write())
            self.limpiar()
            mostrar("Agregación exitosa")

class VentanaMas(Tk):
    def __init__(self,dueño,mascota):
        Toplevel.__init__(self)
        self.title("Mascota: "+mascota.id)
        self.resizable(0,0)
        self.config(bg="#fff")
        self.geometry("800x400")
        self.mascota = mascota

        ftLbl = ("Calibri",12); ftTit = ("Calibri",20); n = "#000"; b = "#fff"
        Label(self,text="Mascota",bg=b,fg=n,font=ftTit).place(x=30,y=15)
        Label(self,text="-"*146,bg=b,fg=n,font=ftLbl).place(x=30,y=56)
        Label(self,text="Codigo:",bg=b,fg=n,font=ftLbl).place(x=50,y=90)
        Label(self,text="Nombre:",bg=b,fg=n,font=ftLbl).place(x=50,y=115)
        Label(self,text="Especie:",bg=b,fg=n,font=ftLbl).place(x=50,y=140)
        Label(self,text="Raza:",bg=b,fg=n,font=ftLbl).place(x=50,y=165)
        Label(self,text="Sexo:",bg=b,fg=n,font=ftLbl).place(x=50,y=190)
        Label(self,text="Edad:",bg=b,fg=n,font=ftLbl).place(x=50,y=215)
        Label(self,text="Dueño:",bg=b,fg=n,font=ftLbl).place(x=50,y=240)
        Label(self,text="Visitas:",bg=b,fg=n,font=ftLbl).place(x=50,y=265)

        cantVisitas = mascota.numeroVisitas()
        Label(self,text=mascota.id,bg=b,fg=n,font=ftLbl).place(x=160,y=90)
        Label(self,text=mascota.nombre,bg=b,fg=n,font=ftLbl).place(x=160,y=115)
        Label(self,text=mascota.especie,bg=b,fg=n,font=ftLbl).place(x=160,y=140)
        Label(self,text=mascota.raza,bg=b,fg=n,font=ftLbl).place(x=160,y=165)
        Label(self,text=mascota.sexo,bg=b,fg=n,font=ftLbl).place(x=160,y=190)
        Label(self,text=mascota.edad,bg=b,fg=n,font=ftLbl).place(x=160,y=215)
        Label(self,text=mascota.dueño,bg=b,fg=n,font=ftLbl).place(x=160,y=240)
        Label(self,text=cantVisitas,bg=b,fg=n,font=ftLbl).place(x=160,y=265)

        self.fec = StringVar()
        Label(self,text="Fecha",bg=b,fg=n,font=ftLbl).place(x=50,y=335)
        self.fech= Entry(self,textvariable=self.fec,highlightcolor="#009",\
            highlightthickness="1",font=ftLbl,width="10")
        self.fech.place(x=160,y=335)

        lin1 = "Introduce la fecha en formato (yyyy/mm/dd). Solo realiza UNA"
        lin2 = "operacion a la vez (agregar baño, corte, atencion y vacuna)."
        lin3 = "Para todas las opciones es necesario introducir al menos fecha."
        lin4 = "NO INTRODUCIR COMAS. "
        Label(self,text=lin1,bg=b,fg="#00f",font=ftLbl).place(x=350,y=90)
        Label(self,text=lin2,bg=b,fg="#00f",font=ftLbl).place(x=350,y=115)
        Label(self,text=lin3,bg=b,fg="#00f",font=ftLbl).place(x=350,y=140)
        Label(self,text=lin4,bg=b,fg="#00f",font=ftLbl).place(x=350,y=165)
        
        self.va, self.at = StringVar(), StringVar()
        Label(self,text="Vacuna:",bg=b,fg=n,font=ftLbl).place(x=350,y=215)
        Label(self,text="Atencion:",bg=b,fg=n,font=ftLbl).place(x=350,y=240)
        self.vac = Entry(self,textvariable=self.va,highlightcolor="#009",\
            highlightthickness="1",font=ftLbl,width="38")
        self.vac.place(x=435,y=215)
        self.ate = Entry(self,textvariable=self.at,highlightcolor="#009",\
            highlightthickness="1",font=ftLbl,width="38")
        self.ate.place(x=435,y=240)

        def atras(): self.destroy(); VentanaCli(dueño)

        atras = Button(self, text="Atras", bg="#900", fg="#fff",\
            width="7", command=atras); atras.place(x=702, y=22)

        regVac = Button(self, text="Agregar Vacuna", width="27",\
            command=self.registrarVacuna); regVac.place(x=350,y=300)
        regAte = Button(self, text="Agregar Atencion",width="27",\
            command=self.registrarAtencion); regAte.place(x=560,y=300)
        regBan = Button(self, text="Agregar Baño", width="27",\
            command=self.registrarBaño); regBan.place(x=350,y=335)
        regCor = Button(self, text="Agregar Corte",width="27",\
            command=self.registrarCorte); regCor.place(x=560,y=335)
    def compFecha(self):
        def esFecha(fecha):
            esAño = esNumero(fecha[:4]) and int(fecha[:4]) >= 2015
            esMes = esNumero(fecha[5:7]) and int(fecha[5:7]) in range(1,13)
            esDia = esNumero(fecha[8:]) and int(fecha[8:]) in range(1,32)
            return esAño and esMes and esDia
        fec = self.fec.get()
        return len(fec)==10 and fec[4]=="/" and fec[7]=="/" and esFecha(fec)
    def noHayComas(self, dato):
        noComas = True
        for letra in dato:
            if letra==",":
                noComas = False; break
        return noComas
    def registrarVacuna(self):
        def c(arreglo):
            return self.va.get()==arreglo[1] and self.mascota.especie==arreglo[0]
        if self.compFecha():
            vacunas = open("vacunas.txt","r").readlines(); existe = False
            for vacuna in vacunas:
                vacuna = vacuna.strip("\n").split(",")
                print(vacuna)
                if c(vacuna) and self.noHayComas(self.va.get()):
                    existe = True; break
            if existe:
                linea = self.mascota.id+","+self.va.get()+","+self.fec.get()+"\n"
                open("mascota_vacuna.txt","a").write(linea)
                self.va.set(""); mostrar("Vacuna puesta en: "+self.fec.get())
            else: mostrar("Vacuna incorrecta")
        else: mostrar("Fecha incorrecta")
    def registrarAtencion(self):
        if self.compFecha():
            if self.noHayComas(self.at.get()) and not esNumero(self.at.get()):
                linea = self.mascota.id+","+self.at.get()+","+self.fec.get()+"\n"
                open("mascota_atencion.txt","a").write(linea)
                self.at.set(""); mostrar("Mascota atendida en: "+self.fec.get())
            else: mostrar("Formato de Atencion incorrecto")
        else: mostrar("Fecha incorrecta")
    def registrarBaño(self):
        if self.compFecha():
            linea = self.mascota.id+","+self.fec.get()+"\n"
            open("mascota_baño.txt","a").write(linea)
            mostrar("Baño registrado en: "+self.fec.get())            
        else:
            mostrar("Fecha incorrecta")
    def registrarCorte(self):
        if self.compFecha():
            linea = self.mascota.id+","+self.fec.get()+"\n"
            open("mascota_corte.txt","a").write(linea)
            mostrar("Corte registrado en: "+self.fec.get())
        else:
            mostrar("Fecha incorrecta")
            
class MostrarCli(Tk):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Mostrar Clientes")
        self.resizable(0,0)
        self.config(bg="#fff")

        ftLbl = ("Calibri",12); ftTit = ("Calibri",20); n = "#000"; b = "#fff"
        Label(self,text="Informacion clientes",bg=b,fg=n,font=ftTit).place(x=30,y=15)
        Label(self,text="-"*84,bg=b,fg=n,font=ftLbl).place(x=30,y=56)

        def show(frame):
            contador=1
            Label(frame,text="  CODIGO  ").grid(row=0,column=0)
            Label(frame,text="        NOMBRE        ").grid(row=0,column=1)
            Label(frame,text="       APELLIDO       ").grid(row=0,column=2)
            Label(frame,text="   SEXO   ").grid(row=0,column=3)
            Label(frame,text="   EDAD   ").grid(row=0,column=4)
            for i in open("clientes.txt","r"):
                k=i.strip("\n").split(',')

                Label(frame,text=k[0]).grid(row=contador,column=0)
                Label(frame,text=k[1]).grid(row=contador,column=1)
                Label(frame,text=k[2]).grid(row=contador,column=2)
                Label(frame,text=k[3]).grid(row=contador,column=3)
                Label(frame,text=k[4]).grid(row=contador,column=4)

                contador+=1

        altura = len(open("clientes.txt","r").readlines())*23
        myframe=Frame(self,bd=1)
        myframe.place(x=50,y=90)
        canvas=Canvas(myframe, height=altura)
        frame = Frame(canvas)

        canvas.pack(side="left")
        canvas.create_window((0,0),window=frame,anchor="nw")

        self.geometry("485x"+str(altura+120))

        show(frame)

        def atras(): self.destroy(); Menu()

        atras = Button(self, text="Atras", bg="#900", fg="#fff",\
            width="7", command=atras); atras.place(x=393, y=22)

class MostrarMas(Tk):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Mostrar Mascotas")
        self.resizable(0,0)
        self.config(bg="#fff")

        ftLbl = ("Calibri",12); ftTit = ("Calibri",20); n = "#000"; b = "#fff"
        Label(self,text="Informacion mascotas",bg=b,fg=n,font=ftTit).place(x=30,y=15)
        Label(self,text="-"*105,bg=b,fg=n,font=ftLbl).place(x=30,y=56)

        def show(frame):
            contador=1
            Label(frame,text="  CODIGO  ").grid(row=0,column=0)
            Label(frame,text="        NOMBRE        ").grid(row=0,column=1)
            Label(frame,text=" ESPECIE. ").grid(row=0,column=2)
            Label(frame,text="         RAZA         ").grid(row=0,column=3)
            Label(frame,text="   SEXO   ").grid(row=0,column=4)
            Label(frame,text="   EDAD   ").grid(row=0,column=5)
            Label(frame,text="   DUEÑO   ").grid(row=0,column=6)
            for i in open("mascotas.txt","r"):
                k=i.strip("\n").split(',')
                
                Label(frame,text=k[0]).grid(row=contador,column=0)
                Label(frame,text=k[1]).grid(row=contador,column=1)
                Label(frame,text=k[2]).grid(row=contador,column=2)
                Label(frame,text=k[3]).grid(row=contador,column=3)
                Label(frame,text=k[4]).grid(row=contador,column=4)
                Label(frame,text=k[5]).grid(row=contador,column=5)
                Label(frame,text=k[6]).grid(row=contador,column=6)
                
                contador+=1

        altura = len(open("mascotas.txt","r").readlines())*22
        myframe=Frame(self,bd=1)
        myframe.place(x=50,y=90)
        canvas=Canvas(myframe,height=str(altura), width="480")
        frame = Frame(canvas)

        canvas.pack(side="left")
        canvas.create_window((0,0),window=frame,anchor="nw")

        self.geometry("590x"+str(altura+120))

        show(frame)

        def atras(): self.destroy(); Menu()

        atras = Button(self, text="Atras", bg="#900", fg="#fff",\
            width="7", command=atras); atras.place(x=498, y=22)

def mostrar(mensaje):
    gen=Toplevel()
    gen.title("Error")
    mesagge=Label(gen,text=mensaje,fg="#000")
    btn=Button(gen,text=" Aceptar ",command=gen.destroy)
    btn.focus_set()
    Label(gen,text="").grid(column=1,row=0)
    Label(gen,text="").grid(column=1,row=2)
    Label(gen,text="").grid(column=1,row=4)
    Label(gen,text=" "*10).grid(column=0,row=0)
    Label(gen,text=" "*10).grid(column=2,row=0)
    mesagge.grid(column=1,row=1)
    btn.grid(column=1,row=3)
    gen.mainloop()    

def nuevoCodigo(archivo):
    lineas = open(archivo,"r").readlines()
    ultimo = lineas[-1].rstrip("\\n").split(",")
    antCod = int(ultimo[0])
    newCod = str(antCod+1)
    return "0"*(4-len(newCod))+newCod

def esNumero(cadena):
    esNumero = True
    for i in cadena:
        if not i in "0123456789":
            esNumero = False; break
    return esNumero

Ingreso()
