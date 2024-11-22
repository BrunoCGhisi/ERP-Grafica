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
            total = 0
            data = request.get_json() # converte em python
            compras = Compras(data['idFornecedor'], data['isCompraOS'], data['dataCompra'], data['numNota'], data['desconto'])
            compras_insumos = data.get('compras_insumos', [])
            financeiro = data.get('financeiros', [])
            

            db.session.add(compras)
            db.session.flush()

            for fin in financeiro:
                parcelas = fin.get("parcelas")  
                forma_pgto = fin.get("idFormaPgto")
                idBanco = fin.get("idBanco")

            for compra in compras_insumos:
                
                idInsumo = compra['idInsumo']
                total += compra['preco'] * (compra['largura'] * compra['comprimento'])

                preco = compra['preco']
                largura = compra['largura']
                comprimento = compra['comprimento']

                insumos = Insumos.query.filter(Insumos.id == idInsumo).all()
                for i in range(len(insumos)):
                    insumo = insumos[i]
                    insumo.estoque += largura * comprimento

                postComprasInsumos = Compras_insumos(compras.id, idInsumo, preco, largura, comprimento)
                db.session.add(postComprasInsumos)


            # FINANCEIRO -------------------------------------- RECEBER
            dataCompra = datetime.strptime(compras.dataCompra, "%Y-%m-%d").date()
            dataVencimento = dataCompra + timedelta(days=30)
            if forma_pgto == 1 or forma_pgto == 2 or forma_pgto == 4:
                descricao = "Compra: " + str(compras.id)+ ", " + "À vista."       
            else:
                descricao = "Compra: " + str(compras.id)+ ", " + "Parcelas: " + str(parcelas) ,
            postFinanceiro = Financeiros(None, compras.id, idBanco, forma_pgto, descricao, 0, total, dataVencimento, compras.dataCompra, None, 0, parcelas)
            db.session.add(postFinanceiro)
                #---------------------------------------------------

            db.session.commit()
            return 'Compras adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            dataCompras = Compras.query.all()
           
            dataCompras_insumos = Compras_insumos.query.all()
            
            newDataCompras = {'compras': [compra.to_dict() for compra in dataCompras]}

            newDataCompras_insumos = {'compras_insumos': [compra_insumo.to_dict() for compra_insumo in dataCompras_insumos]} #pegando cada obj compra, e tranformando num dicionario
           
            idCompra = []
            fkCompra = []
            getComprasI = {"compra_insumo": []}

            for compra_insumo in newDataCompras_insumos['compras_insumos']:
                fkCompra.append(compra_insumo['idCompra']) 

            for compra in newDataCompras['compras']:
                idCompra.append(compra['id'])
                
              
                for idV in idCompra:
                    for fkV in fkCompra:
                        if fkV == idV:
                            getCompras = [compra.to_dict() for compra in dataCompras]
                            getComprasI =[compra_insumo.to_dict() for compra_insumo in dataCompras_insumos]
                            
                        else:
                            getCompras = [compra.to_dict() for compra in dataCompras]
                            

            return {
                "compras": getCompras,
                "comprasInsumos": getComprasI
            }, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                compra = Compras.query.get(id)
                data = request.get_json() #pega todos os dados
                dataCompras_insumos = data.get('compras_insumos', []) #preciso pegar os ID's disso aqui, passa no json           
                dataFinanceiros = data.get('financeiros', [])
                 # PUT EM FINANCEIROS ---------------------------
                financeiros = Financeiros.query.filter(Financeiros.idCompra == id).all()
                for i in range(len(financeiros)):
                    financeiro = financeiros[i]
                    fin_data = dataFinanceiros[i]
                    print(fin_data)

                    financeiro.parcelas = fin_data.get('parcelas', financeiro.parcelas)
                    financeiro.idFormaPgto = fin_data.get('idFormaPgto', financeiro.idFormaPgto)
                    print(financeiro.idFormaPgto)

                    if financeiro.idFormaPgto != 1 and financeiro.idFormaPgto != 2 and financeiro.idFormaPgto != 4:     
                        descricao = "Compra: " + str(id)+ ", " + "Parcelas: " + str(fin_data.get('parcelas', financeiro.parcelas))
                    else:
                         descricao = "Compra: " + str(compra.id)+ ", " + "À vista."   
                    financeiro.descricao = descricao
                    financeiro.idBanco = fin_data.get('idBanco', financeiro.idBanco)
                    
                # PUT EM VP ---------------------------
                compras_insumos = Compras_insumos.query.filter(Compras_insumos.idCompra == id).all()

                for i in range(len(compras_insumos)):
                    compra_insumo = compras_insumos[i]
                    ci_data = dataCompras_insumos[i]

                    compra_insumo.idInsumo = ci_data.get('idInsumo', compra_insumo.idInsumo)
                    compra_insumo.largura = ci_data.get('largura', compra_insumo.largura)
                    compra_insumo.comprimento = ci_data.get('comprimento', compra_insumo.comprimento)
                    compra_insumo.preco = ci_data.get('preco', compra_insumo.preco)

                
                if compra is None:
                    return{'error': 'compra não encontrado'}, 405
                
                compra.idFornecedor = data.get('idFornecedor', compra.idFornecedor)
                compra.isCompraOS = data.get('isCompraOS', compra.isCompraOS)   
                compra.dataCompra = data.get('dataCompra', compra.dataCompra)   
                compra.numNota = data.get('numNota', compra.numNota)   
                compra.desconto = data.get('desconto', compra.desconto)
  

                db.session.commit()
                return "compra atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o compra. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            compra = Compras.query.get(id) # vai procurar compras NO BANCO com esse id

            dataCompras_insumos = Compras_insumos.query.all()
            newDataCompras_insumos = {'compras_insumos': [compra_produto.to_dict() for compra_produto in dataCompras_insumos]} #pegando cada obj compra, e tranformando num dicionario
            
            for produto in newDataCompras_insumos['compras_insumos']:
               
                if int(produto['idCompra']) == int(id):
                    
                    prodObj = Compras_insumos.query.get(produto['id'])
                    db.session.delete(prodObj)
            

            finfilter = Financeiros.query.filter(Financeiros.idCompra == id).first()
            if finfilter is None:
                pass    
            else:
                db.session.delete(finfilter)
            
            if compra is None:
                return{'error': 'compra não encontrado'}, 405
            
            db.session.delete(compra)
            db.session.commit()
            return "compra deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o compra. Erro:{str(e)}", 405
        

