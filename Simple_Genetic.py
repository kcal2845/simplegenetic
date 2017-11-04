import random

# 유전자 개수,길이,유전자 범위, 변이율
geneEA = 20
geneLeng = 20
genescale = list()
mutation = 50

geneEA = int(input('개체 개수 : '))
geneLeng = int(input('유전자 길이 : '))
mutation = int(input('변이율 : '))

genescale.append(int(input('유전자 범위 : ')))
genescale.append(int(input('유전자 범위 : ')))
print('선택된 유전자 범위 %d ~ %d \n'%(genescale[0],genescale[1]))


# 타겟 유전자
target = list()
print('타겟 유전자를 설정합니다.')
for i in range(0,geneLeng):

    inputs = int(input('%d번째 유전자:'%(i+1)))
    if inputs >= genescale[0] and inputs <= genescale[1] :
        target.append(inputs)
        
    else :
        exit()
        
print('\n타겟으로 설정된 유전자 : '+str(target))
input('엔터키를 누르면 초기 유전자를 설정합니다.\n')


genes = list()
parents = list()
fitness = list()

# 초기 유전자 설정
print('genes initialization\n')
for i in range(0,geneEA):
    genes.append([random.choice(range(genescale[0], genescale[1]+1)) for _ in range(geneLeng)])

# 세대
generation = 0 
while True:
    
    # 부모유전자, 선택도 초기화
    parents = list()
    fitness = list()
    print('\n----------')
    print('\n%d 세대'%(generation))

    for i in range(0,geneEA):
        print(str(genes[i]))

    # 선택
    for i in range(0,geneEA):
        fitness.append(0)
        
        # 타겟 유전자와 비교
        for f in range(0,geneLeng):
            if(genes[i][f] != target[f]):
                fitness[i] = fitness[i] + abs(target[f] - genes[i][f])

    # 적합도가 낮은 번호 부터 순위
    rank = sorted(range(geneEA), key = lambda k: fitness[k])
    
    for i in range(0,geneEA):
        parents.append(genes[rank[i]])
        
    parents = parents[0:int(geneEA/3)]

    for i in range(0,int(geneEA/3)):
        print('다음세대 부모 유전자 : '+str(parents[i]))

    # 교차
    for i in range(0,geneEA):
        selected = list()
        # 리스트 두개 랜덤으로 고름
        selected = random.sample(parents,2)

        # 랜덤으로 부모유전자 물려받음
        for f in range(0,geneLeng):
            if(random.choice(range(0,2)) == 0):
                genes[i][f] = selected[0][f]
            else:
                genes[i][f] = selected[1][f]


    # 변이
    for i in range(0,geneEA):
        for f in range(0,geneLeng):

            if(random.randrange(0,mutation) == 0):
                # 원래 유전자값을 제외한 값만 랜덤으로 고르기
                lst = list(filter( lambda x: x != genes[i][f], list( range(genescale[0],genescale[1]+1) )))
                genes[i][f] = random.choice(lst)
                print('돌연 변이 발생!')

        
    
    generation = generation +1 # 세대 올림
    input('\n엔터키를 누르면 다음세대로 넘어갑니다.')
