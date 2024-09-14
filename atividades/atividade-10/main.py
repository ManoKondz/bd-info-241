    from fastapi import FastAPI, HTTPException
    import mysql.connector

    app = FastAPI()

    # Função para obter a conexão com o banco de dados MySQL
    def get_db_connection():
        return mysql.connector.connect(
            host="localhost",  # Ajuste conforme seu ambiente
            user="root",
            password="rootpassword",
            database="escola"
        )

    # Função para criar o banco de dados e a tabela TB_ALUNOS se não existirem
    def init_db():
        conn = mysql.connector.connect(
            host="localhost",  # Ajuste conforme seu ambiente
            user="root",
            password="rootpassword"
        )
        cursor = conn.cursor()

        # Criação do banco de dados
        cursor.execute("CREATE DATABASE IF NOT EXISTS escola")

        # Usar o banco de dados criado
        cursor.execute("USE escola")

        # Criação da tabela TB_ALUNOS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TB_ALUNOS (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                faltas INT DEFAULT 0,
                N1 DECIMAL(5, 2) DEFAULT 0.00,
                N2 DECIMAL(5, 2) DEFAULT 0.00,
                Aprovado_SN BOOLEAN DEFAULT FALSE
            )
        """)

        # Inserção de dados de exemplo, caso a tabela esteja vazia
        cursor.execute("SELECT COUNT(*) FROM TB_ALUNOS")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO TB_ALUNOS (nome, faltas, N1, N2)
                VALUES (%s, %s, %s, %s)
            """, [
                ('João Silva', 10, 7.5, 8.0),
                ('Maria Oliveira', 5, 9.0, 8.5),
                ('Pedro Santos', 25, 4.0, 5.5),
                ('Ana Costa', 18, 6.0, 6.5)
            ])
        
        conn.commit()
        cursor.close()
        conn.close()

    # Inicializar o banco de dados ao iniciar a API
    @app.on_event("startup")
    def startup_event():
        init_db()

    # Rota para listar os alunos
    @app.get("/alunos")
    def listar_alunos():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Selecionar todos os alunos
            cursor.execute("SELECT nome, Aprovado_SN FROM TB_ALUNOS")
            alunos = cursor.fetchall()

            # Preparar resultado como uma lista de dicionários
            resultado = [{"nome": nome, "status": "APROVADO" if aprovado else "REPROVADO"} for nome, aprovado in alunos]

            cursor.close()
            conn.close()

            return {"alunos": resultado}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar alunos: {e}")

    # Rota para aprovar alunos
    @app.post("/aprovar-alunos")
    def aprovar_alunos():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Selecionar todos os alunos da tabela TB_ALUNOS
            cursor.execute("SELECT id, nome, faltas, N1, N2 FROM TB_ALUNOS")
            alunos = cursor.fetchall()

            for aluno in alunos:
                aluno_id, nome, faltas, N1, N2 = aluno
                aprovado = (faltas < 20) and ((N1 + N2) / 2 >= 6.0)  # Regra de aprovação

                # Atualizar status de aprovação no banco de dados
                cursor.execute(
                    "UPDATE TB_ALUNOS SET Aprovado_SN = %s WHERE id = %s",
                    (1 if aprovado else 0, aluno_id)
                )

            # Confirmar as atualizações
            conn.commit()
            cursor.close()
            conn.close()

            return {"message": "Status de aprovação atualizado com sucesso!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao aprovar alunos: {e}")