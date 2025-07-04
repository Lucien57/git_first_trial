import random

# 打印矩阵函数
def matrix_print(obj):
    for i in obj:
        for j in i:
            print(j,end='  ')
        print('\n')

reverse=lambda coor:[coor[1],coor[0]]

class WordSearch:
    # 接受4四个参数：puzzle的大小(横向纵向各一个参数)、题目中字母的范围、目标词语
    def __init__(self,x,y,letters,target):
        self.xSize=int(x)
        self.ySize=int(y)
        self.letterRange=letters
        self.targetWord=target
        mid=[]
        for i in range(y):
            for j in range(x):
                mid.append([j,i])
        self.coord=mid  # 一个对应于问题的坐标列表。

    # 输入一个坐标，输出其所有相邻点的坐标构成的列表,不会超出方阵
    # 若输入的坐标为空，返回矩阵中所有点坐标构成的列表(方便开始)
    def find_environs(self, coor):
        if not coor:  # 起始点返回所有坐标
            return self.coord

        r, c = coor
        neighbors = [
            [r - 1, c], [r + 1, c],  # 上下
            [r, c - 1], [r, c + 1]  # 左右
        ]
        # 过滤无效坐标，不能用pop！否则会跳过索引。
        # 例：list=[0,1,2,3]，我要去掉list中的第0和第2个元素
        # 若代码为：list.pop(0);list.pop(2),实际剩下的是[1,2](Why?)
        return [
            [nr, nc] for nr, nc in neighbors
            if 0 <= nr < self.ySize and 0 <= nc < self.xSize
        ]

    # 生成随机题目
    def generate(self):
        record=dict([(i,self.letterRange[i]) for i in range(len(self.letterRange))])
        puzzle=[]
        for m in range(self.ySize):
            line=[]
            for n in range(self.xSize):
                line.append(record[random.randint(0,len(self.letterRange)-1)])
            puzzle.append(line)
        return puzzle

    # 题目说明环节
    def explain(self,puzzle):
        with open('explain',mode='r'):pass
        print("See the details in the file 'explain'.")
        print('The puzzle:')
        matrix_print(puzzle)
        print('Target:%s'%self.targetWord)

    '''如何定义这个csp问题？
    variables:解的坐标列表
    domain:self.coord
    constraints:填写的坐标在puzzle中对应的字母不可以与self.targetWord不同！注意，只否定不同的情况，
    若坐标未填写不算violate the constraints.'''

    def if_consistent(self,puzzle,values):
        for i in values:
            # 填到一半也能通过。
            if puzzle[i[0]][i[1]]!= self.targetWord(values.index(i)) and i!=[]:
                return False
        return True

    def csp(self, puzzle):
        """回溯搜索求解：返回目标单词在矩阵中的坐标路径（如果存在）"""

        # 获取目标单词长度
        n = len(self.targetWord)

        # 处理特殊情况：空单词直接返回空路径
        if n == 0:
            return []

        # 处理特殊情况：单词长度超过矩阵容量，不可能存在解
        if n > self.xSize * self.ySize:
            return None

        # 创建访问标记矩阵，记录每个位置是否已使用
        # 和那个到达四角问题一样，用T/F的列表记录访问过的节点。
        visited = [[False] * self.xSize for _ in range(self.ySize)]

        # 存储当前搜索路径的坐标列表
        path = []

        # 定义内部回溯函数（递归搜索）
        def backtrack(index):
            """
            递归回溯函数
            :param index: 当前需要匹配的目标单词中的字符索引
            :return: 如果找到完整路径则返回路径列表，否则返回None
            """
            # 基础情况：已匹配所有字符，返回完整路径
            if index == n:
                return path.copy()  # 返回路径的副本，避免后续修改影响结果

            # 处理目标单词的第一个字符（起始点）
            if index == 0:
                # 遍历矩阵中所有位置
                for r in range(self.ySize):
                    for c in range(self.xSize):
                        # 检查当前位置是否匹配目标单词的首字母
                        if puzzle[r][c] == self.targetWord[index]:
                            # 标记当前位置已访问
                            visited[r][c] = True
                            # 将当前位置添加到路径中
                            path.append([r, c])

                            # 递归搜索下一个字符
                            res = backtrack(index + 1)

                            # 如果找到解，直接返回
                            if res:
                                return res

                            # 回溯：移除当前位置，尝试其他可能性
                            path.pop()
                            visited[r][c] = False
                # 所有可能起始点都尝试过但未找到解
                return []

            # 处理目标单词的后续字符（非起始点）
            else:
                # 获取路径中最后一个位置（当前字符的前一个位置）
                r0, c0 = path[-1]

                # 获取当前位置的所有有效邻居
                for nr, nc in self.find_environs([r0, c0]):
                    # 检查邻居位置是否未访问且匹配目标字符
                    if not visited[nr][nc] and puzzle[nr][nc] == self.targetWord[index]:
                        # 标记邻居位置已访问
                        visited[nr][nc] = True
                        # 将邻居位置添加到路径
                        path.append([nr, nc])

                        # 递归搜索下一个字符
                        res = backtrack(index + 1)

                        # 如果找到解，直接返回
                        if res:
                            return res

                        # 回溯：移除邻居位置，尝试其他可能性
                        path.pop()
                        visited[nr][nc] = False

                # 当前路径的所有邻居都尝试过但未找到解
                return []

        # 从目标单词的第一个字符开始搜索
        return backtrack(0)

    def print_solution(self,solution,puzzle)->None:
        flip= [reverse(j) for j in solution]
        for i in self.coord:
            if i[0]==0:print('\n')
            if i in flip: print(puzzle[i[1]][i[0]],end='  ')
            else: print('x',end='  ')

def game_main():
    game= WordSearch(7,7,'fourt','four')
    puzzle= game.generate()
    game.explain(puzzle)
    solution=game.csp(puzzle)
    response=input('Your answer:')
    if response not in ['Yes!','No!']:
        raise ValueError('Not a valid answer!')
    if response=='Yes!'and solution!=[] or response=='No!'and solution==[]:
        print('Good job!')
    else:
        print('Pity~ Not correct!')
    if solution!=[]:game.print_solution(solution,puzzle)

def analyze():
    game = WordSearch(7, 7, 'fourt', 'four')
    success=0
    for i in range(1000000):
        puzzle= game.generate()
        success += 1 if game.csp(puzzle) != [] else 0
    return success/1000000

#玩找词游戏。
#game_main()

#估算有解的概率。
#possibility=analyze()
#print(possibility)
