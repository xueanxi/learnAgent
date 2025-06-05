from sentence_transformers import SentenceTransformer

# 加载预训练模型
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# 验证模型是否正确加载
print("模型维度:", embed_model.get_sentence_embedding_dimension())
# 输出: 模型维度: 384 (所有文档和查询都应编码为384维向量)