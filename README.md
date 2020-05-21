# TODO

- local sqs 설치
- local dynamodb 설치
- local lambda invoke
- local 에서 람다를 실행시킨 후 다시 sqs 에 queue 를 생성한 후 다시 lambda 를 실행시키는 로직 작성

## 왜?

serverless framwork를 사용해 보면서 로컬 세팅이 의외로 어렵고 메뉴얼이 잘 되어 있지 않는 부분이 있어서 공유하기 위해 해당 자료를 제작하게 되었다.

## 사전 준비

1. npm 또는 yarn 설치: [npm 소개와 설치 (About Node Package Manager) | 프로그래밍 요람에서 무덤까지](https://web-front-end.tistory.com/3)
2. docker 설치: [초보를 위한 도커 안내서 - 설치하고 컨테이너 실행하기](https://subicura.com/2017/01/19/docker-guide-for-beginners-2.html)
3. aws cli 설치: [Mac awscli 설치법](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/install-cliv2-mac.html)
4. serverless 와 aws lambda에 대한 약간의 사전 이해

## 시작하기

```
npm install
```

## sqs를 로컬에서 실행하기 위한 방법

아래와 같은 스크립트로 로컬에서 실행.

#### 1. 플러그인 설치

sqs offline 으로 실행하기 위해서는 `sls plugin install -n serverless-offline-sqs`로 로컬 서버리스 패키지 설치

#### 2. Elasticmq 로컬 실행

```
docker run -p 9324:9324 softwaremill/elasticmq
```

#### 3. sls offline 실행

로컬에서 `Docker Container`로 `elasticmq` 실행 후 `sls offline`를 실행해줘야 함. 만약, `Docker`가 아닌 로컬에서 elasticmq 를 통해 sqs를 실행하려 한다면 이 [링크](https://github.com/softwaremill/elasticmq) 를 참조.

## dynamodb 를 로컬에서 실행하기 위한 방법

#### 설치하기

1. `sls plugin install -n serverless-dynamo-local` 스크립트로 설치를 진행한다.
2. `sls dynamodb install`을 통해서 로컬에 설치 후 `sls dynamodb start`를 실행

## Serverless.yml 설정

```
service: sls-crawler

provider:
  name: aws
  runtime: python3.8
  stage: dev
  region: ap-northeast-2

  iamRoleStatements:
    - Effect: "Allow"
      Action:
        - "s3:ListBucket"
      Resource:
        {
          "Fn::Join":
            ["", ["arn:aws:s3:::", { "Ref": "ServerlessDeploymentBucket" }]],
        }
    - Effect: "Allow"
      Action:
        - "s3:PutObject"
      Resource:
        Fn::Join:
          - ""
          - - "arn:aws:s3:::"
            - "Ref": "ServerlessDeploymentBucket"
            - "/*"

functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: hello
          method: get
  sqs_test:
    handler: handler.sqs_hello
    events:
      - sqs:
          queueName: MyTestQueue
          arn:
            Fn::GetAtt:
              - MyTestQueue
              - Arn
  call_sqs:
    handler: handler.call_sqs
    events:
      - http:
          path: call_sqs
          method: get

plugins:
  - serverless-python-requirements
  - serverless-offline-sqs
  - serverless-dynamodb-local
  - serverless-offline

custom:
  pythonRequirements:
    dockerizePip: true
  serverless-offline-sqs:
    autoCreate: true # Queue 가 없을 시 만들 것
    apiVersion: "2012-11-05"
    endpoint: http://0.0.0.0:9324
    region: ap-northeast-2
    accessKeyId: root
    secretAccessKey: root
    skipCacheInvalidation: false
  dynamodb:
    # 특정한 스테이지 DynamoDB local 실행 정의
    stages:
      - dev
    start:
      port: 9000
      inMemory: true
      heapInitial: 200m
      heapMax: 1g
      migrate: true
      seed: true
      convertEmptyValues: true
    # DynamoDB를 로컬에서 이미 실행중인 경우는 아래 주석 제거
    # noStart: true

resources:
  Resources:
    MyTestQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: MyTestQueue

    usersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: usersTable
        AttributeDefinitions:
          - AttributeName: email
            AttributeType: S
        KeySchema:
          - AttributeName: email
            KeyType: HASH
        ProvisionedThroughput:
          ReadCapacityUnits: 1
          WriteCapacityUnits: 1
```

## 참고 링크

- [serverless-dynamodb-local - npm](https://www.npmjs.com/package/serverless-dynamodb-local)
- [AWS re:Invent 특집2 – 서버리스Serverless 마이크로서비스를 위한 일곱 가지 모범 사례 윤석찬](https://www.slideshare.net/awskorea/recap2016-2-7-best-practices-microservices?next_slideshow=1)
- [SQS, Lambda를 이용해 문자전송하기(1부) | Seha's Devlog](https://sehajyang.github.io/2019/09/25/sqs-lambda-python/)
- [초보를 위한 도커 안내서 - 설치하고 컨테이너 실행하기](https://subicura.com/2017/01/19/docker-guide-for-beginners-2.html)
- [npm 소개와 설치 (About Node Package Manager) | 프로그래밍 요람에서 무덤까지](https://web-front-end.tistory.com/3)
