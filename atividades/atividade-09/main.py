import mysql.connector

# Conectar ao banco de dados MySQL
conn = mysql.connector.connect(
    host = "172.19.0.1",  # ou o IP do contêiner do banco de dados
    user = "root",
    password = "mypassworld",
    database="escola"
)

cursor = conn.cursor()

# Selecionar todos os alunos da tabela TB_ALUNOS
cursor.execute("SELECT id, nome, faltas, N1, N2 FROM TB_ALUNOS")
alunos = cursor.fetchall()

# Iterar sobre os registros e aplicar a lógica de aprovação
for aluno in alunos:
    aluno_id, nome, faltas, N1, N2 = aluno
    aprovado = True  # Inicialmente, considerar aprovado
    
    # Verificar faltas
    if faltas >= 20:
        aprovado = False
    # Verificar média
    elif (N1 + N2) / 2 < 6.0:
        aprovado = False

    # Atualizar status de aprovação no banco de dados
    cursor.execute(
        "UPDATE TB_ALUNOS SET Aprovado_SN = %s WHERE id = %s",
        (aprovado, aluno_id)
    )
    conn.commit()

# Exibir os alunos e o status final de aprovação
cursor.execute("SELECT nome, Aprovado_SN FROM TB_ALUNOS")
resultados = cursor.fetchall()

print("Status de Aprovação dos Alunos:")
for nome, aprovado in resultados:
    status = "APROVADO" if aprovado else "REPROVADO"
    print(f"Aluno: {nome} - Status: {status}")

# Fechar conexão com o banco de dados
cursor.close()
conn.close()
