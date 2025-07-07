import pandas as pd

df = pd.read_csv("tabla.csv",delimiter=';')

tablaLatex = df.to_latex(caption="Tabla de transiciones del NFA",label="tab:transiciones",longtable=True,index=False,escape=True)

with open("tabla.tex", "w") as f:
    f.write(tablaLatex)
