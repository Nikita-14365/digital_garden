import tkinter as tk
from math import sin, cos, pi
from PIL import Image, ImageTk
from random import random, randint, uniform


#DNA: [DNA0, DNA1]
#DNA0: [[[gene0, gene1]...]...]
#DNA1: [[len, angle, position,
#        [start_width, start_rotation, start_soft, start_red, start_green, start_blue],
#        [end_width, end_rotation, end_soft, end_red, end_green, end_blue],
#        [parent_width, parent_rotation, parent_soft, parent_red, parent_green, parent_blue],
#        [random_width, random_rotation, random_soft, random_red, random_green, random_blue]]...]
# #49561d; #47571d

class Branch:
    def __init__(self, tree, parent, DNA, gene0, gene1, gens, rand):
        self.tree = tree
        self.parent = parent
        self.DNA = DNA
        self.gene0 = gene0
        self.gene1 = gene1
        self.gens = gens
        self.rand = rand()
        if gens > 0:
            self.children = [Branch(tree, self, DNA, g0, g1, gens-1, rand) for g0, g1 in DNA[0][gene0]]
        else:
            self.children = []

    def get_gene0(self):
        return self.DNA[0][self.gene0]

    def get_gene1(self):
        return self.DNA[1][self.gene1]

class Tree:
    def __init__(self, DNA, gens, Branch, rand=None):
        self.DNA = DNA
        self.gens = gens
        if rand is None:
            self.rand = random
        else:
            self.rand = rand
        self.root = Branch(self, None, DNA, 0, 0, gens, self.rand)

class TreeView:
    def __init__(self, canvas, tree):
        self.tree = tree
        self.canvas = canvas
        self.shapes = []
        self.circles = []
        #self.bbox_id = canvas.create_rectangle(0, 0, canvas.winfo_reqwidth(), canvas.winfo_reqheight(), fill="green")
        #self.pot_pool = canvas.create_rectangle(-50, -50, 50, 50, fill="red", tag="a")
        self.pot_image = Image.open("pot.png")
        self.pot_resized = self.pot_image.resize((100, 100))
        self.pot_tk = ImageTk.PhotoImage(self.pot_resized)
        self.pot = canvas.create_image(0, 0, image=self.pot_tk, tag="a")

    def draw(self):
        pot = self.canvas.coords(self.pot)
        self.draw_branch(pot[0], pot[1]-self.pot_resized.size[1]*0.4, 0, 10, 0, 0, 100, 100, 100, self.tree.root, 0)
        print("size", self.pot_image.size[1])

    def draw_branch(self, X, Y, A, W, T, S, R, G, B, branch, I):
        print("branch")
        length, angle, position, start, end, parent, rand = branch.get_gene1()
        sw, st, ss, sr, sg, sb = start
        ew, et, es, er, eg, eb = end
        pw, pt, ps, pr, pg, pb = parent
        rw, rt, rs, rr, rg, rb = rand
        #w = (branch.parent.get_gene1()[3][0]*(1-position) + branch.apent.get_energy1()[4][0]*position)*pw + sw*(1-pw)
        #t = (branch.parent.get_gene1()[3][1]*(1-position) + branch.apent.get_energy1()[4][1]*position)*pt + sw*(1-pt)
        #s = (branch.parent.get_gene1()[3][2]*(1-position) + branch.apent.get_energy1()[4][2]*position)*ps + sw*(1-ps)
        #r = (branch.parent.get_gene1()[3][3]*(1-position) + branch.apent.get_energy1()[4][3]*position)*pr + sw*(1-pr)
        #g = (branch.parent.get_gene1()[3][4]*(1-position) + branch.apent.get_energy1()[4][4]*position)*pg + sw*(1-pg)
        #b = (branch.parent.get_gene1()[3][5]*(1-position) + branch.apent.get_energy1()[4][5]*position)*pb + sw*(1-pb)
        w = W*pw + sw*(1-pw)
        t = T*pt + st*(1-pt)
        s = S*ps + ss*(1-ps)
        r = R*pr + sr*(1-pr)
        g = G*pg + sg*(1-pg)
        b = B*pb + sb*(1-pb)
        ws = (ew - w) / length
        ts = (et - t) / length
        ss_= (es - s) / length
        rs = (er - r) / length
        gs = (eg - g) / length
        bs = (eb - b) / length
        A += branch.get_gene1()[1]
        for i in range(length):
            #w = (sw*(i+I) + (branch.parent.get_gene1()[]*pw + ew*(1-pw))*(length-(i+I))) / length
            #r = (sr*(i+I) + er)
            if i+I < len(self.shapes) and False:
                self.circles[i+I] = [X, Y, A, w, t, s, r, g, b]
                self.canvas.coords(self.shapes[(i+I)*3], X - w/2 - 1, Y - w/2 - 1, X + w/2 - 1, Y + w/2 - 1)
                self.canvas.coords(self.shapes[(i+I)*3 + 1], X - w/2, Y - w/2, X + w/2, Y + w/2)
                self.canvas.coords(self.shapes[(i+I)*3 + 2], X - w/2 + 1, Y - w/2 + 1, X + w/2 + 1, Y + w/2 + 1)
                self.canvas.itemconfig(self.shapes[(i+I)*3], fill=byte_to_hex(int(r+20), int(g + 20), int(b + 20)))
                self.canvas.itemconfig(self.shapes[(i+I)*3 + 1], fill=byte_to_hex(int(r), int(g), int(b)))
                self.canvas.itemconfig(self.shapes[(i+I)*3 + 2], fill=byte_to_hex(int(r-20), int(g - 20), int(b - 20)))
            else:
                self.circles.append([X, Y, A, w, t, s, r, g, b])
                self.shapes.append(self.canvas.create_oval(X - w/2 - 1, Y - w/2 - 1, X + w/2 - 1, Y + w/2 - 1, width=0, tag="a"))
                self.shapes.append(self.canvas.create_oval(X - w/2, Y - w/2, X + w/2, Y + w/2, width=0, tag="a"))
                self.shapes.append(self.canvas.create_oval(X - w/2 + 1, Y - w/2 + 1, X + w/2 + 1, Y + w/2 + 1, width=0, tag="a"))
                self.canvas.itemconfig(self.shapes[(i+I)*3], fill=byte_to_hex(int(r+20), int(g+20), int(b+20)))
                self.canvas.itemconfig(self.shapes[(i+I)*3 + 1], fill=byte_to_hex(int(r), int(g), int(b)))
                self.canvas.itemconfig(self.shapes[(i+I)*3 + 2], fill=byte_to_hex(int(r-20), int(g-20), int(b-20)))
            X += 1 * sin(A)
            Y -= 1 * cos(A)
            A += t
            A %= 2*pi
            if pi + s <= A <= pi - s and s > 0:
                A = pi
            elif (A <= s or A >= 2*pi - s) and s < 0:
                A = 0
            else:
                A += s
            w += ws
            t += ts
            s += ss_
            r += rs
            g += gs
            b += bs
        i = 0
        for b in branch.children:
            i += self.draw_branch(*self.circles[I + int(length*b.get_gene1()[2]*0.9)], b, I+i+length)
        return length + i

    def scale(self):
        #x0, y0, x1, y1 = self.canvas.coords(self.shapes[0])
        #self.canvas.coords(self.pot, (x0+x1)/2 - self.pot_image.size[0]*0, (y0+y1)/2 + 0.5*self.pot_image.size[1])
        #x, y = self.canvas.coords(self.shapes[0])[:2]
        w = self.canvas.winfo_width() / self.canvas.winfo_reqwidth()
        h = self.canvas.winfo_height() / self.canvas.winfo_reqheight()
        #self.canvas.scale((x0+x1)/2, (y0+y1)/2, min(w, h), min(w, h))
        print(self.canvas.coords(self.pot))
        x0, y0, x1, y1 = self.canvas.bbox("all")
        print("1")
        #self.canvas.scale("all", *self.canvas.coords(self.pot), min(w, h), min(w, h))
        s = min((x1-x0)/self.canvas.winfo_reqwidth(), (y1-y0)/self.canvas.winfo_reqheight(), 10)
        print("2")
        #self.canvas.scale("all", (x0+x1)/2, (y0+y1)/2, (1/s)/2, (1/s)/2)
        print("3", int(self.pot_image.size[0]*s), int(self.pot_image.size[1]*s), s, self.canvas.bbox("all"))
        self.pot_resized = self.pot_image.resize((int(self.pot_image.size[0]*s), int(self.pot_image.size[1]*s)))
        print("4")
        self.pot_tk = ImageTk.PhotoImage(self.pot_resized)
        print(5)
        self.canvas.itemconfig(self.pot, image=self.pot_tk)
        #self.canvas.coords(self.pot, (x0+x1)/2 - self.pot_image.size[0]*0, (y0+y1)/2 + self.pot_resized.size[1])

        print(6)
        self.canvas.move("all", (self.canvas.winfo_reqwidth() - (x0+x1)/2)/2, (self.canvas.winfo_reqheight() - (y0+y1)/2)/2)
        print(7)
        print(self.canvas.coords(self.pot), s, (x0+x1)/2, (y0+y1)/2, self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight())

    def scale(self):
        x0, y0, x1, y1 = self.canvas.bbox("a")
        w = self.canvas.winfo_reqwidth()
        h = self.canvas.winfo_reqheight()
        sx = w / (x1 - x0)
        sy = h / (y1 - y0)
        s = min(sx, sy)
        if s == 0:
            print("zero scale")
            return
        self.canvas.coords(self.bbox_id, *self.canvas.bbox("a"))
        #print("!!", self.canvas.bbox("a"), s, sx, sy, x1 - x0, y1 - y0, (x1 + x0)/2, (y1 + y0)/2, w/2 - (x1 + x0)/2, h/2 - (y1 + y0)/2)
        #input("...")
        self.canvas.scale("a", (x1 + x0)/2, (y1 + y0)/2, s, s)
        self.pot_resized = self.pot_image.resize((round(self.pot_resized.size[0] * s), round(self.pot_resized.size[1] * s)))
        self.canvas.coords(self.bbox_id, *self.canvas.bbox("a"))
        x0, y0, x1, y1 = self.canvas.bbox("a")
        #self.canvas.scale("all", 1/s, 1/s, 0, 0)
        #print("!!", self.canvas.bbox("a"), s, sx, sy, x1 - x0, y1 - y0, (x1 + x0)/2, (y1 + y0)/2, w/2 - (x1 + x0)/2, h/2 - (y1 + y0)/2)
        #input("...")
        x0, y0, x1, y1 = self.canvas.bbox("a")
        self.canvas.move("a", w/2 - (x1 + x0)/2, h/2 - (y1 + y0)/2)
        self.canvas.coords(self.bbox_id, *self.canvas.bbox("a"))
        x0, y0, x1, y1 = self.canvas.bbox("a")
        w = self.canvas.winfo_reqwidth()
        h = self.canvas.winfo_reqheight()
        sx = w / (x1 - x0)
        sy = h / (y1 - y0)
        s = min(sx, sy)
        print("!!", self.canvas.bbox("a"), s, sx, sy, x1 - x0, y1 - y0, (x1 + x0)/2, (y1 + y0)/2, w/2 - (x1 + x0)/2, h/2 - (y1 + y0)/2)

    def scale(self):
        x0, y0, x1, y1 = self.canvas.bbox("a")
        w = self.canvas.winfo_reqwidth()
        h = self.canvas.winfo_reqheight()

        #self.canvas.coords(self.bbox_id, self.canvas.bbox("a"))
        #input("...")

        self.canvas.move("a", w/2 - (x1 + x0)/2, h/2 - (y1 + y0)/2)

        x0, y0, x1, y1 = self.canvas.bbox("a")
        sx = w / (x1 - x0)
        sy = h / (y1 - y0)
        s = min(sx, sy)

        #self.canvas.coords(self.bbox_id, self.canvas.bbox("a"))
        #input("...")

        self.canvas.scale("a", (x1 + x0)/2, (y1 + y0)/2, s, s)
        #self.canvas.coords(self.bbox_id, self.canvas.bbox("all"))
        #input("...")


        self.pot_resized = self.pot_image.resize((round(self.pot_resized.size[0] * s), round(self.pot_resized.size[1] * s)))
        self.pot_tk = ImageTk.PhotoImage(self.pot_resized)
        self.canvas.itemconfig(self.pot, image=self.pot_tk)

        #self.canvas.coords(self.bbox_id, self.canvas.bbox("a"))

        b = self.canvas.bbox("a")
        #self.canvas.coords(self.bbox_id, *b)
        print(x1-x0, y1-y0, (x1-x0)*s, (y1-y0)*s, b[2]-b[0], b[3]-b[1])

    def reset(self):
        self.pot_resized = self.pot_image.resize((100, 100))
        self.pot_tk = ImageTk.PhotoImage(self.pot_resized)
        self.canvas.itemconfig(self.pot, image=self.pot_tk)
        for i in self.shapes:
            self.canvas.delete(i)
        self.canvas.coords(self.pot, 0, 0)
        #self.canvas.coords(self.pot_pool, -50, -50, 50, 50)
        self.circles.clear()
        self.shapes.clear()
    def __del__(self):
        for s in self.shapes:
            try:
                self.canvas.delete(s)
            except:
                pass
        try:
            self.canvas.delete(self.pot)
        except:
            pass

class ScrollFrame(tk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.rowconfigure(0, weight=1)
        #self.columnconfigure(0, weight=1)
        #self.columnconfigure(2, weight=1)
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.scrollbar.pack(fill="y", side="right", expand="false")
        #self.scrollbar.grid(row=0, column=1)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")
        #self.canvas.grid(row=0, column=0)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.interior = tk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=self.interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)

def byte_to_hex(r, g, b):
    r = ("0" + hex(r)[2:])[-2:]
    g = ("0" + hex(g)[2:])[-2:]
    b = ("0" + hex(b)[2:])[-2:]
    return "#" + r + g + b

root = tk.Tk()

root.bind("<Escape>", lambda x: root.destroy())

canvas = tk.Canvas(root, width=1000, height=1000, bg="black")
canvas.pack()

#DNA = [[[[0, 0]]],
#       [[10, 30, 0, [1 for i in range(6)], [1 for i in range(6)], [1 for i in range(6)], [1 for i in range(6)]]]]

DNA = [[[[0, 0]]],
       [[10, 0.5, 0.5, [3, 0, 0, 120, 120, 120], [3, 0, 0, 50, 50, 50], [0.9, 0, 0, 0.9, 0.5, 0.1], [0, 0, 0, 0, 0, 0]]]]
def random_DNA():
    len0 = randint(1, 10)
    len1 = randint(1, 10)
    len0 = len1 = 10
    DNA = [[[[randint(0, len0-1), randint(0, len1-1)] for j in range(max(0, randint(0, 3)))] for i in range(len0)],
            [[randint(100, 300), uniform(-pi/36, +pi/36), random()] + [[randint(2, 15), uniform(-pi/36, +pi/36), uniform(-pi/36, +pi/36), randint(20, 200), randint(20, 200), randint(20, 200)] for n in range(2)] + 
             [[random() for m in range(6)]] + [[0]*6] for i in range(len1)]]
    print(DNA[1][0])

    return DNA

button = tk.Button(root, text="new DNA", command=lambda: exec("global DNA; DNA = random_DNA(); treeview.tree = Tree(DNA, 5, Branch); treeview.reset(); treeview.draw(); treeview.scale()"))
button.pack()

print("start")
DNA = random_DNA()
print("step")
tree = Tree(DNA, 5, Branch, lambda: None)
print("tree")
treeview = TreeView(canvas, tree)
print("draw")
treeview.draw()
print(canvas.bbox("all"), canvas.winfo_width(), canvas.winfo_height(), canvas.winfo_reqwidth(), canvas.winfo_reqheight())
treeview.scale()
print("scale")
#canvas.scale("all", -100, -100, 5, 5)

if __name__ == "__main__":
    root.mainloop()
