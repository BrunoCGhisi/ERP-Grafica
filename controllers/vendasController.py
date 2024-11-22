from flask import request
from database.db import db
from models.vendas import Vendas
from models.vendas_produtos import Vendas_produtos
from models.produtos import Produtos
from models.insumos import Insumos
from models.financeiros import Financeiros
from datetime import timedelta, datetime

descControl = 0
def vendasController():


    if request.method == 'POST':
        try:

            info = ""
            data = request.get_json() # converte em python
            vendas = Vendas(data['idCliente'], data['idVendedor'], data['dataAtual'], data['isVendaOS'], data['situacao'], data['desconto'])
            vendas_produtos = data.get('vendas_produtos', [])
            financeiro = data.get('financeiro', [])

            db.session.add(vendas)
            db.session.flush() # para conseguir pegar id
            total = 0
            
            for fin in financeiro:
                parcelas = fin.get("parcelas")  
                forma_pgto = fin.get("idFormaPgto")
                idBanco = fin.get("idBanco")


            for objVp in vendas_produtos: # Dando post em vendas_produtos
                idProduto = objVp['idProduto']
                quantidade = objVp.get('quantidade')  # Retorna None se 'quantidade' não existe
                produtos = Produtos.query.filter(Produtos.id == objVp['idProduto']).all()
                for item in produtos:
                    gastoEstoque = (item.largura * item.comprimento) * quantidade
                    insumos = Insumos.query.filter(Insumos.id == item.idInsumo).all()
                    for ins in insumos:
                        if ins.estoque <= gastoEstoque:
                            info = f'{ins.nome} não possui estoque o suficiente! Reponha para produção.'
                    total += quantidade * item.preco # calcula o valor total da venda
                    
                postVendasProdutos = Vendas_produtos(vendas.id, idProduto, quantidade)
                db.session.add(postVendasProdutos)

            # FINANCEIRO -------------------------------------- RECEBER
            dataVenda = datetime.strptime(vendas.dataAtual, "%Y-%m-%d").date()
            dataVencimento = dataVenda + timedelta(days=30)
            if forma_pgto == 1 or forma_pgto == 2 or forma_pgto == 4:
                descricao = "Venda: " + str(vendas.id)+ ", " + "À vista."       
            else:
                descricao = "Venda: " + str(vendas.id)+ ", " + "Parcelas: " + str(parcelas)
           
            postFinanceiro = Financeiros(vendas.id, None, idBanco, forma_pgto, descricao, 1, total, dataVencimento, vendas.dataAtual, None, 0, parcelas)
            db.session.add(postFinanceiro)
            #---------------------------------------------------
            
            db.session.commit()
            return {
                "message":  'Vendas adicionados com sucesso!',
                "info": info   
            }, 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            descControl += 1
            print(descControl)
            dataVendas = Vendas.query.all()
           
            dataVendas_produtos = Vendas_produtos.query.all()
            
            newDataVendas = {'vendas': [venda.to_dict() for venda in dataVendas]}

            newDataVendas_produtos = {'vendas_produtos': [venda_produto.to_dict() for venda_produto in dataVendas_produtos]} #pegando cada obj venda, e tranformando num dicionario
           
            idVenda = []
            fkVenda = []
            getVendasP = {"vendas_produto": []}

            for venda_produto in newDataVendas_produtos['vendas_produtos']:
                fkVenda.append(venda_produto['idVenda']) 

            for venda in newDataVendas['vendas']:
                idVenda.append(venda['id'])
                
              
                for idV in idVenda:
                    for fkV in fkVenda:
                        if fkV == idV:
                            getVendas = [venda.to_dict() for venda in dataVendas]
                            getVendasP =[venda_produto.to_dict() for venda_produto in dataVendas_produtos]
                            
                        else:
                            getVendas = [venda.to_dict() for venda in dataVendas]
                            

            return {
                "vendas": getVendas,
                "vendasProdutos": getVendasP
            }, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405    

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                venda = Vendas.query.get(id)
                data = request.get_json() #pega todos os dados 
                dataVendas_produtos = data.get('vendas_produtos', []) #preciso pegar os ID's disso aqui, passa no json           
                dataFinanceiros = data.get('financeiro', [])
                

                # PUT EM FINANCEIROS ---------------------------
                financeiros = Financeiros.query.filter(Financeiros.idVenda == id).all()
                for i in range(len(financeiros)):
                    financeiro = financeiros[i]
                    fin_data = dataFinanceiros[i]
                    print(fin_data)

                    financeiro.parcelas = fin_data.get('parcelas', financeiro.parcelas)
                    financeiro.idFormaPgto = fin_data.get('idFormaPgto', financeiro.idFormaPgto)
                    print(financeiro.idFormaPgto)

                    if financeiro.idFormaPgto != 1 and financeiro.idFormaPgto != 2 and financeiro.idFormaPgto != 4:     
                        descricao = "Venda: " + str(id)+ ", " + "Parcelas: " + str(fin_data.get('parcelas', financeiro.parcelas))
                    else:
                         descricao = "Venda: " + str(venda.id)+ ", " + "À vista."   
                    financeiro.descricao = descricao
                    financeiro.idBanco = fin_data.get('idBanco', financeiro.idBanco)
                # PUT EM VP ---------------------------
                vendas_produtos = Vendas_produtos.query.filter(Vendas_produtos.idVenda == id).all()

                for i in range(len(vendas_produtos)):
                    venda_produto = vendas_produtos[i]
                    vp_data = dataVendas_produtos[i]

                    venda_produto.idProduto = vp_data.get('idProduto', venda_produto.idProduto)
                    venda_produto.quantidade = vp_data.get('quantidade', venda_produto.quantidade)

                    db.session.commit()  
                
                if venda is None:
                    return{'error': 'venda não encontrado'}, 405
                
                venda.idCliente = data.get('idCliente', venda.idCliente)
                venda.dataAtual = data.get('dataAtual', venda.dataAtual)   
                venda.isVendaOS = data.get('isVendaOS', venda.isVendaOS)   

                if data.get('situacao', venda.situacao) >= 2:
        
                    allVendasProd = Vendas_produtos.query.filter(Vendas_produtos.idVenda == id).all()
                    
                    for obj in allVendasProd:
                    
                        idProduto = obj.idProduto
                        quantidade = obj.quantidade

                        dataProd = Produtos.query.get(idProduto)
                        insumos = Insumos.query.filter(Insumos.id == dataProd.idInsumo).all()
                        for ins in insumos:
                            if (quantidade * (dataProd.largura * dataProd.comprimento)) > ins.estoque or ins.estoque == 0:
                                return f'Estoque insuficiente para a produção do produto: {dataProd.nome} , reponha!', 200

                        dataInsumo = Insumos.query.get(dataProd.idInsumo)
                        desc = quantidade * (dataProd.largura * dataProd.comprimento)

                        dataInsumo.estoque -= dataInsumo.estoque - desc

                if data.get('situacao', venda.situacao) < 2:
                    pass
                
                venda.desconto = data.get('desconto', venda.desconto)
                venda.situacao = data.get('situacao', venda.situacao)
     
                db.session.commit()

                return "venda atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar a venda. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            data = int(request.args.to_dict().get('id'))  # Obtém o ID da venda a ser deletada
            venda = Vendas.query.get(data)  # Procura a venda no banco de dados

            if venda is None:
                return {'error': 'venda não encontrada'}, 404

            # Remover produtos associados
            produtos = Vendas_produtos.query.filter_by(idVenda=data).all()
            for produto in produtos:
                db.session.delete(produto)

            financeiros = Financeiros.query.filter_by(idVenda=data).all()
            for financeiro in financeiros:
                db.session.delete(financeiro)

            # Deletar a venda
            db.session.delete(venda)
            db.session.commit()
            return "venda deletada com sucesso", 202

        except Exception as e:
            db.session.rollback()  
            return f"Não foi possível apagar a venda. Erro: {str(e)}", 500

        

