from flask import request
from database.db import db
from models.vendas import Vendas
from models.vendas_produtos import Vendas_produtos
from models.produtos import Produtos
from models.insumos import Insumos

def vendasController():

    if request.method == 'POST':
        try:

            data = request.get_json() # converte em python
            vendas = Vendas(data['idCliente'], data['idVendedor'], data['data'], data['isVendaOS'], data['situacao'], data['desconto'])
            vendas_produtos = data.get('vendas_produtos', [])

            db.session.add(vendas)
            db.session.flush() # para conseguir pegar id
            
            for objVp in vendas_produtos:
                idProduto = objVp['idProduto']
                quantidade = objVp['quantidade']
                postVendasProdutos = Vendas_produtos(vendas.id, idProduto, quantidade)
                db.session.add(postVendasProdutos)
            
            db.session.commit()
            return 'Vendas adicionados com sucesso!', 200
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

            for venda_produto in newDataVendas_produtos['vendas_produtos']:
                fkVenda.append(venda_produto['idVenda']) 

            for venda in newDataVendas['vendas']:
                idVenda.append(venda['id'])

                for idV in idVenda:
                    for fkV in fkVenda:
                        if fkV == idV:
                            getVendas = {'vendas':[[venda.to_dict() for venda in dataVendas],[venda_produto.to_dict() for venda_produto in dataVendas_produtos]]}
                        else:
                            getVendas = {'vendas':[venda.to_dict() for venda in dataVendas]}

            
            return getVendas, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405    

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                venda = Vendas.query.get(id)
                data = request.get_json() #pega todos os dados 
                dataVendas_produtos = data.get('vendas_produtos', []) #preciso pegar os ID's disso aqui, passa no json           

                for venda_produto in dataVendas_produtos:
                    id_vp = venda_produto.get('id')
                    #print("produto", produto)
                    vendas_produtos = Vendas_produtos.query.filter(Vendas_produtos.idVenda == id).all()
                    #print(vendas_produtos)
                    #print(len(vendas_produtos))
                        
                    for produto_vp in vendas_produtos:
                        
                        #print(id_vp)
                        #print(produto_vp.id)
                        if produto_vp.id == id_vp:
                            #print("OOOOLOKO")
                            produto_vp.idProduto = produto.get('idProduto')
                            produto_vp.quantidade = produto.get('quantidade')                       
                            db.session.commit()  
                

                if venda is None:
                    return{'error': 'venda não encontrado'}, 405
                
                venda.idCliente = data.get('idCliente', venda.idCliente)
                venda.idVendedor = data.get('idVendedor', venda.idVendedor)   
                venda.data = data.get('data', venda.data)   
                venda.isVendaOS = data.get('isVendaOS', venda.isVendaOS)   
                venda.situacao = data.get('situacao', venda.situacao)

                if data.get('situacao', venda.situacao) == 5:
        
                    allVendasProd = Vendas_produtos.query.filter(Vendas_produtos.idVenda == id).all()
                    
                    for obj in allVendasProd:
                    
                        idProduto = obj.idProduto
                        quantidade = obj.quantidade

                        dataProd = Produtos.query.get(idProduto)
                        print("nome: ",dataProd.nome)
                        print("insumo: ",dataProd.idInsumo)
                        print("tamanho: ",dataProd.tamanho)
                        print("quant:",quantidade)
                        print(20*"-")

                        dataInsumo = Insumos.query.get(dataProd.idInsumo)
                        desc = quantidade * dataProd.tamanho
                        print(desc)
                        dataInsumo.estoque = dataInsumo.estoque - desc
                        
                    print(allVendasProd)
                    
                    print("estoque vai mudar")
                
                venda.desconto = data.get('desconto', venda.desconto)
     
                db.session.commit()

                return "venda atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar a venda. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            venda = Vendas.query.get(id) # vai procurar vendas NO BANCO com esse id

            dataVendas_produtos = Vendas_produtos.query.all()
            newDataVendas_produtos = {'vendas_produtos': [venda_produto.to_dict() for venda_produto in dataVendas_produtos]} #pegando cada obj venda, e tranformando num dicionario
            
            for produto in newDataVendas_produtos['vendas_produtos']:
                if int(produto['idVenda']) == int(id):
                    vendas_produtos = Vendas_produtos.query.get(produto['id'])
                    db.session.delete(vendas_produtos)

            if venda is None:
                return{'error': 'venda não encontrado'}, 405
            
            db.session.delete(venda)
            db.session.commit()
            return "venda deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o venda. Erro:{str(e)}", 405
        

