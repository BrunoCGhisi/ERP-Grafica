from flask import request
from database.db import db
from models.formas_pgto import Formas_pgto


def formas_pgtoController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            formas_pgto = Formas_pgto(data['tipo'], data['idBanco'])
            db.session.add(formas_pgto)
            db.session.commit()
            return 'Formas_pgto adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Formas_pgto.query.all()
            newData = {'formas_pgto': [forma_pgto.to_dict() for forma_pgto in data]} #pegando cada obj forma_pgto, e tranformando num dicionario
            if len(data) <= 1:

                if len(data) == 1: 
                    db.session.add(Formas_pgto("Débito"))
                    db.session.add(Formas_pgto("Crédito"))
                    db.session.add(Formas_pgto("Pix"))
                    db.session.add(Formas_pgto("Boleto"))
                    db.session.add(Formas_pgto("À prazo"))
                    db.session.add(Formas_pgto("Cheque"))
                    db.session.commit()
                elif len(data) == 0:
                    db.session.add(Formas_pgto("Dinheiro"))
                    db.session.add(Formas_pgto("Débito"))
                    db.session.add(Formas_pgto("Crédito"))
                    db.session.add(Formas_pgto("Pix"))
                    db.session.add(Formas_pgto("Boleto"))
                    db.session.add(Formas_pgto("À prazo"))
                    db.session.add(Formas_pgto("Cheque"))
                    db.session.commit()

            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                forma_pgto = Formas_pgto.query.get(id)
                data = request.get_json() #pega todos os dados

                if forma_pgto is None:
                    return{'error': 'Forma_pgto não encontrado'}, 405
                
                forma_pgto.tipo = data.get('tipo', forma_pgto.tipo)
                forma_pgto.idBanco = data.get('idBanco', forma_pgto.idBanco)   

                db.session.commit()
                return "Forma_pgto atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o forma_pgto. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            forma_pgto = Formas_pgto.query.get(id) # vai procurar formas_pgto NO BANCO com esse id

            if forma_pgto is None:
                return{'error': 'Forma_pgto não encontrado'}, 405
            
            db.session.delete(forma_pgto)
            db.session.commit()
            return "Forma_pgto deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o forma_pgto. Erro:{str(e)}", 405
        

