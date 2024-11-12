from flask import request
from database.db import db
from models.vendas import Vendas
from models.vendas_produtos import Vendas_produtos
from models.produtos import Produtos
from models.insumos import Insumos
from models.financeiros import Financeiros
from datetime import timedelta, datetime

def vendasController():

    if request.method == 'POST':
        try:

            info = ""
            data = request.get_json() # converte em python
            vendas = Vendas(data['idCliente'], data['idVendedor'], data['dataAtual'], data['isVendaOS'], data['situacao'], data['desconto'])
            vendas_produtos = data.get('vendas_produtos', [])
            print(vendas_produtos)
            parcelas = data.get('parcelas', []) # parcelas
            forma_pgto = data.get('idForma_pgto', []) # id
            idBanco = data.get('idBanco', [])

            db.session.add(vendas)
            db.session.flush() # para conseguir pegar id
            total = 0

            for objVp in vendas_produtos: # Dando post em vendas_produtos
                idProduto = objVp['idProduto']
                quantidade = objVp.get('quantidade')  # Retorna None se 'quantidade' não existe
                produtos = Produtos.query.filter(Produtos.id == objVp['idProduto']).all()
                for item in produtos:
                    gastoEstoque = item.tamanho * quantidade
                    insumos = Insumos.query.filter(Insumos.id == item.idInsumo).all()
                    for ins in insumos:
                        if ins.estoque <= gastoEstoque:
                            info = f'{ins.nome} não possui estoque o suficiente! Reponha para produção.'
                    total += quantidade * item.preco # calcula o valor total da venda
                    print(vendas.id, idProduto, quantidade)
                postVendasProdutos = Vendas_produtos(vendas.id, idProduto, quantidade)
                db.session.add(postVendasProdutos)

            # FINANCEIRO -------------------------------------- RECEBER
            dataVenda = datetime.strptime(vendas.dataAtual, "%Y-%m-%d").date()
            dataVencimento = dataVenda + timedelta(days=30)
            if forma_pgto == 1 or forma_pgto == 2 or forma_pgto == 4:
                descricao = "Venda: " + str(vendas.id)+ ", " + "À vista."       
            else:
                descricao = "Venda: " + str(vendas.id)+ ", " + "Parcelas: " + str(parcelas) ,
            postFinanceiro = Financeiros(vendas.id, idBanco, forma_pgto, descricao, 1, total, dataVencimento, vendas.dataAtual, "", 0, 0, parcelas)
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
                "vendas_produtos": getVendasP
            }, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405    

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                venda = Vendas.query.get(id)
                data = request.get_json() #pega todos os dados 
                dataVendas_produtos = data.get('vendas_produtos', []) #preciso pegar os ID's disso aqui, passa no json           

                # PUT EM FINANCEIROS TAMBÉM
                financeiro = Financeiros.query.filter(Financeiros.idVenda == id).all()
                print(financeiro)
                financeiro.parcelas = data.get('parcelas', financeiro.parcelas)
                financeiro.idBanco = data.get('idBanco', financeiro.idBanco)
                financeiro.idFormaPgto = data.get('idFormaPgto', financeiro.idFormaPgto) 

                for venda_produto in dataVendas_produtos:
                    id_vp = venda_produto.get('id')

                    vendas_produtos = Vendas_produtos.query.filter(Vendas_produtos.idVenda == id).all()

                    for produto_vp in vendas_produtos:
                        if produto_vp.id == id_vp:
                            produto_vp.idProduto = produto.get('idProduto')
                            produto_vp.quantidade = produto.get('quantidade')                       
                            db.session.commit()  
                
                if venda is None:
                    return{'error': 'venda não encontrado'}, 405
                
                venda.idCliente = data.get('idCliente', venda.idCliente)
                venda.dataAtual = data.get('dataAtual', venda.dataAtual)   
                venda.isVendaOS = data.get('isVendaOS', venda.isVendaOS)   

                if data.get('situacao', venda.situacao) == 4:
        
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
                        desc = quantidade * dataProd.tamanho
                        
                        dataInsumo.estoque = dataInsumo.estoque - desc
                        
                
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

        

