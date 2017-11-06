import random

# 유전 클래스
class genetic:
    
    # -- 변수 초기화 --
    def __init__(self,target, population=10, genemin=0 ,genemax=255, sequencelength=3,mutationrate=50):
    
        self.population = population # 개체 개수
        self.genemin = genemin # 한 유전자의 범위 최소값
        self.genemax = genemax # 한 유전자의 범위 최대값
        self.sequencelength = sequencelength # 유전자의 길이
        self.target = target # 타겟 유전자
        self.mutationrate = mutationrate
        
        self.genes = list()
        self.fitness = list()
        self.parents = list()
        self.crossovered = list()
        self.mutated = list()
        self.rank = list()
        
        self.generation = -1
        

    # -- 메인 메서드 --
    
    # 초기화
    def initpopulation(self):
        # 초기 유전자 설정
        self.genes = list()
        for i in range(0,self.population):
            self.genes.append([random.choice(range(self.genemin,self.genemax+1)) for _ in range(self.sequencelength)])
        self.generation = 0
        return True
            
    # 다음세대
    def nextgeneration(self):
        if self.generation < 0:
            return False

        self.generation = self.generation + 1
        
        # 선택
        self.parents = self.selection()
        
        # 교배
        self.crossovered = self.crossover()
        
        # 변이
        self.mutated = self.mutation()

        # 대치 (미구현)
        self.genes = self.mutated

        # 평가
        self.fitness,self.rank = self.fitnessrank(self.genes,self.target,self.population)
        return True
    
    # -- 유전 기능 메서드 --

    # 0. 적합도 순위 - 타겟과 직접 유전자 비교
    def fitnessrank(self,genes,target,population):
        genes = self.genes
        target = self.target
        population = self.population
        sequencelength = self.sequencelength
        
        fitness = list()
        rank = list()
        
        for i in range(0,population):
            fitness.append(0)
        
            # 타겟 유전자와 비교
            for f in range(sequencelength):
                if(genes[i][f] != target[f]):
                    fitness[i] = fitness[i] + abs(target[f] - genes[i][f])
                    
        # 적합도가 낮은 번호 부터 순위
        rank = sorted(range(population), key = lambda k: fitness[k])
        return fitness,rank

    # 0. 적합도 순위 - 타겟 상수 비교 (미구현)
    
    #1. 선택 - 순위 기반 
    def selection(self):
        
        genes = self.genes
        target = self.target
        population = self.population
        
        parents = list()
        fitness = list()
        rank = list()
        
        fitness,rank = self.fitnessrank(genes,target,population)

        # 우선순위부터 정렬
        for i in range(0,population):
            parents.append(genes[rank[i]])

        # 정렬 뒤 앞의 1/2만 자름
        parents = parents[0:int(population/2)]
        
        return parents

    #2. 교배 - 다점 교배(?)
    def crossover(self):
        genes = self.genes
        parents = self.parents
        population = self.population
        sequencelength = self.sequencelength
         
        for i in range(0,population):
            selected = list()
           # 리스트 두개 랜덤으로 고름
            selected = random.sample(parents,2)

           # 랜덤으로 부모유전자 물려받음
            for f in range(sequencelength):
                if(random.choice(range(0,2)) == 0):
                    genes[i][f] = selected[0][f]
                else:
                    genes[i][f] = selected[1][f]
                    
        return genes
        
    
    #3. 변이 - 변이
    def mutation(self):
        population = self.population
        mutationrate = self.mutationrate
        genemin = self.genemin
        genemax = self.genemax
        sequencelength = self.sequencelength
        crossovered = self.crossovered
        
        for i in range(population):
            for f in range(sequencelength):

                if(random.randrange(0,mutationrate) == 0):
                    # 원래 유전자값을 제외한 값만 랜덤으로 고르기
                    lst = list(filter( lambda x: x != crossovered[i][f], list( range(genemin,genemax+1) )))
                    crossovered[i][f] = random.choice(lst)

        return crossovered
    
    #4.  대치 - 아직 미구현

    # -- 기타 메서드 --
    
    # 현재 유전자 출력
    def printgenes(self):
        if self.generation == 0:
            print('\n[ 초기 유전자]')
        else:
            print('\n[ '+ str(self.generation)+ ' 세대 유전자]')
            
        for i in range(self.population):
            print(str(self.genes[i]))
            
# 리스트 평균 구하는 함수
def average(list):
    return (sum(list) / len(list))

# -- 메인 --
population = int(input('개체 개수 : '))
mutationrate = int(input('변이율 : '))
sequencelength = int(input('유전자 길이 : '))
genemin = int(input('유전자 범위 최소값 : '))
genemax = int(input('유전자 범위 최대값 : '))

target = list()
print('타겟 유전자를 설정합니다.')
for i in range(sequencelength):

    inputs = int(input('%d번째 유전자:'%(i+1)))
    if inputs >= genemin and inputs <= genemax :
        target.append(inputs)
        
    else :
        exit()

print('\n타겟으로 설정된 유전자 : '+str(target))
input('엔터키를 누르면 초기 유전자를 설정합니다.\n')
              
sample = genetic(population = population,mutationrate=mutationrate,genemin = genemin, genemax=genemax, target=target)
sample.initpopulation()
sample.printgenes()
input('엔터로 다음 세대')

while(sample.nextgeneration()):
    if(sample.parents[0] == sample.target):
        print('샘플에서 타겟과 100퍼센트 같은 유전자가 나왔습니다!')
        break
    
    sample.printgenes()
    print('최고 유전자 : ' + str(sample.parents[0]))
    print('최고 유전자 적합도 : ' + str(sample.fitness[sample.rank[0]]))
    print('전체 적합도 평균 : ' + str(average(sample.fitness)))
    
    input('엔터')



