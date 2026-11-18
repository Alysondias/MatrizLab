
# =====================================
# MATRIZLAB
# Multiplicação de Matrizes
# =====================================

from flask import Flask, render_template, request

# Criando a aplicação
app = Flask(__name__)


# =====================================
# 1. LER UMA MATRIZ
# =====================================

def ler_matriz(texto):

    linhas = texto.strip().split("\n")

    matriz = []

    for linha in linhas:

        valores = linha.split()

        numeros = []

        for valor in valores:
            numeros.append(float(valor))

        matriz.append(numeros)

    # Verificar se todas as linhas possuem
    # a mesma quantidade de colunas

    quantidade_colunas = len(matriz[0])

    for linha in matriz:

        if len(linha) != quantidade_colunas:
            raise ValueError("Todas as linhas devem ter a mesma quantidade de números.")

    return matriz


def multiplicar_matrizes(A, B):

    # Verificar se a multiplicação é possível

    if len(A[0]) != len(B):
        raise ValueError(
            "A quantidade de colunas da Matriz A "
            "deve ser igual à quantidade de linhas da Matriz B."
        )

    resultado = []
    passos = []

    # Percorrer as linhas da Matriz A

    for i in range(len(A)):

        linha_resultado = []

        # Percorrer as colunas da Matriz B

        for j in range(len(B[0])):

            soma = 0
            calculos = []

            # Multiplicar os elementos correspondentes

            for k in range(len(B)):

                produto = A[i][k] * B[k][j]

                soma = soma + produto

                # Formatar os números da explicação

                a = int(A[i][k]) if A[i][k].is_integer() else A[i][k]
                b = int(B[k][j]) if B[k][j].is_integer() else B[k][j]

                calculos.append(f"({a} x {b})")

            # Remover casas decimais do resultado inteiro

            if soma.is_integer():
                soma = int(soma)

            linha_resultado.append(soma)

            # Guardar a explicação de cada posição

            passos.append({
                "posicao": f"C[{i+1},{j+1}]",
                "calculo": " + ".join(calculos),
                "resultado": soma
            })

        resultado.append(linha_resultado)

    return resultado, passos

# =====================================
# 3. PÁGINA PRINCIPAL
# =====================================

@app.route("/")
def inicio():

    return render_template("index.html")

# =====================================
# 4. RECEBER DADOS E CALCULAR
# =====================================

@app.route("/multiplicar", methods=["POST"])
def multiplicar():

    try:

        # Receber as matrizes enviadas pelo HTML

        texto_a = request.form.get("matriz_a", "")
        texto_b = request.form.get("matriz_b", "")

        # Transformar os textos em matrizes

        A = ler_matriz(texto_a)
        B = ler_matriz(texto_b)

        # Realizar a multiplicação

        resultado, passos = multiplicar_matrizes(A, B)

        # Enviar o resultado para o HTML

        return render_template(
    "index.html",
    resultado=resultado,
    passos=passos
)
        

    except (ValueError, IndexError) as erro:

        return render_template(
            "index.html",
            erro=str(erro)
        )


# =====================================
# 5. EXECUTAR O PROGRAMA
# =====================================

if __name__ == "__main__":

    app.run(debug=True)
