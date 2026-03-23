# Backend Skills Starter

这是一个基于 **Python 标准库** 的轻量后端应用模板，包含：

- 健康检查接口 `/health`
- 简单的 Todo CRUD 接口 `/todos`
- skill 列表接口 `/skills`
- 一个可复用的基础后端 skill：`skills/backend-api-baseline`

## 快速启动

```bash
python -m app.main
```

启动后可访问：

- `GET /health`
- `GET /skills`
- `GET /todos`
- `POST /todos`
- `POST /todos/{item_id}/complete`
- `DELETE /todos/{item_id}`

### 示例请求

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/todos -H 'Content-Type: application/json' -d '{"title":"ship skill"}'
```

## 测试

```bash
python -m unittest discover -s tests
```

## Skill 用途

`backend-api-baseline` 适用于后续扩展新的后端资源：

- 新增 CRUD feature
- 补齐 service 层与输入校验
- 生成基础测试骨架
- 统一接口结构与开发检查清单
