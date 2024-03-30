.PHONY: format lint all layer layer-deploy clean

format:
	black .

lint:
	flake8 .

fl: format lint

image:
	aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 000505334922.dkr.ecr.ap-northeast-1.amazonaws.com
	docker build -t vectordb_base_gpt .
	docker tag vectordb_base_gpt:latest 000505334922.dkr.ecr.ap-northeast-1.amazonaws.com/vectordb_base_gpt:latest
	docker push 000505334922.dkr.ecr.ap-northeast-1.amazonaws.com/vectordb_base_gpt:latest

deploy: image
	aws lambda update-function-code --function-name vectordb-based-gpt --image-uri 000505334922.dkr.ecr.ap-northeast-1.amazonaws.com/vectordb_base_gpt:latest
