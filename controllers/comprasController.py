from flask import request
from database.db import db
from models.compras import Compras
from models.insumos import Insumos
from models.financeiros import Financeiros
from models.compras_insumos import Compras_insumos
from datetime import timedelta, datetime


def comprasController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            total = 0
            #Perguntar pro belone se eu preciso fazer a parte de verificar quem é forncedor no back ou se eu só filtro isso no front-end
            compras = Compras(data['idFornecedor'], data['isCompraOS'], data['dataCompra'], data['numNota'], data['desconto'], data['isOpen'])
            compras_insumos = data.get('compras_insumos', [])
            parcelas = data.get('parcelas', []) # parcelas
            forma_pgto = data.get('idForma_pgto', []) # id
            idBanco = data.get('idBanco', [])

            db.session.add(compras)
            db.session.flush()

            for compra in compras_insumos:
                
                idInsumo = compra['idInsumo']
                allInsumos = Insumos.query.filter(Insumos.id == idInsumo).all()

                total += compra['preco'] * (compra['largura'] * compra['comprimento'])

                if len(allInsumos) == 0:
                    nome = compra['idInsumo']
                    estoque = (compra['largura'] * compra['comprimento'])
                    isActive = 1
                    postInsumo = Insumos(nome, estoque, isActive)
                    db.session.add(postInsumo)
                    db.session.flush()
                    postComprasInsumos = Compras_insumos(compras.id, postInsumo.id, compra['preco'], compra['largura'], compra['comprimento'])
                    db.session.add(postComprasInsumos)

                else:
                    preco = compra['preco']
                    largura = compra['largura']
                    comprimento = compra['comprimento']

                    postComprasInsumos = Compras_insumos(compras.id, idInsumo, preco, largura, comprimento)
                    db.session.add(postComprasInsumos)


                # # FINANCEIRO -------------------------------------- RECEBER
                # dataVenda = datetime.strptime(compras.dataAtual, "%Y-%m-%d").date()
                # dataVencimento = dataVenda + timedelta(days=30)
                # if forma_pgto == 1 or forma_pgto == 2 or forma_pgto == 4:
                #     descricao = "Compra: " + str(compras.id)+ ", " + "À vista."       
                # else:
                #     descricao = "Venda: " + str(compras.id)+ ", " + "Parcelas: " + str(parcelas) ,
                # postFinanceiro = Financeiros(compras.id, idBanco, forma_pgto, descricao, 1, total, dataVencimento, compras.dataAtual, compras.dataAtual, 0, 0, parcelas)
                # db.session.add(postFinanceiro)
                # #---------------------------------------------------

            db.session.commit()
            return 'Compras adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Compras.query.all()
            newData = {'compras': [compra.to_dict() for compra in data]} #pegando cada obj compra, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                compra = Compras.query.get(id)
                data = request.get_json() #pega todos os dados
                print("PUTPUYPUT", data)

                
                if compra is None:
                    return{'error': 'compra não encontrado'}, 405
                
                compra.idFornecedor = data.get('idFornecedor', compra.idFornecedor)
                compra.isCompraOS = data.get('isCompraOS', compra.isCompraOS)   
                compra.dataCompra = data.get('dataCompra', compra.dataCompra)   
                compra.numNota = data.get('numNota', compra.numNota)   
                compra.desconto = data.get('desconto', compra.desconto)
                compra.isOpen = data.get('isOpen', compra.isOpen) 

                db.session.commit()
                return "compra atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o compra. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            compra = Compras.query.get(id) # vai procurar compras NO BANCO com esse id

            dataCompras_insumos = Compras_insumos.query.all()
            newDataCompras_insumos = {'compras_insumos': [compra_produto.to_dict() for compra_produto in dataCompras_insumos]} #pegando cada obj venda, e tranformando num dicionario
            
            for produto in newDataCompras_insumos['compras_insumos']:
                if int(produto['idCompra']) == int(id):
                    prodObj = Compras_insumos.query.get(produto['id'])
                    db.session.delete(prodObj)


            if compra is None:
                return{'error': 'compra não encontrado'}, 405
            
            db.session.delete(compra)
            db.session.commit()
            return "compra deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o compra. Erro:{str(e)}", 405
        

