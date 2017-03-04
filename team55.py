import sys
import copy
import random


class Player55():
	def __init__(self):
        	self.CELL_WEIGHT = [[3, 2, 2, 3],[2, 4, 4, 2],[2, 4, 4, 2],[3, 2, 2, 3]]
		self.SUM_ALL_CELLS_WEIGHT = 40
		self.TIE = 0
		self.WIN_GAME_SCORE = 40*40
		self.inf=9999999
		self.neg_inf=-9999999
		self.APPROXIMATE_WIN_SCORE = 14
	    	self.BIG_BOARD_WEIGHT = 39
	    	self.WIN_SCORE = 10**6
	    	self.POSSIBLE_WIN_SEQUENCES = [((0,0),(0,1),(0,2),(0,3)),((1,0),(1,1),(1,2),(1,3)),((2,0),(2,1),(2,2),(2,3)),
									((3,0),(3,1),(3,2),(3,3)),((0,0),(1,0),(2,0),(3,0)),((0,1),(1,1),(2,1),(3,1)),
									((0,2),(1,2),(2,2),(3,2)),((0,3),(1,3),(2,3),(3,3)),((0,0),(1,1),(2,2),(3,3)),
									((0,3),(1,2),(2,1),(3,0))]
	def move(self, board, old_move, flag):

		current_board = [[0 for i in range(16)]for j in range(16)]
        	current_block_status = [[0 for i in range(4)]for j in range(4)]
        	# empty: 0, ourmove: 1, opponentmove: 2
        	for i in range(16):
            		for j in range(16):
                			if board.board_status[i][j] == flag:
                   		 		current_board[i][j] = 1;
               				elif board.board_status[i][j] == '-':
                    				current_board[i][j] = 0;
                			else :
                    				current_board[i][j] = 2;

        	for i in range(4):
            		for j in range(4):
                		if board.block_status[i][j] == flag:
                    			current_block_status[i][j] = 1;
                		elif board.block_status[i][j] == '-':
                    			current_block_status[i][j] = 0;
                		elif board.block_status[i][j] == 'd':
                    			current_block_status[i][j] = 3;
                		else :
                    			current_block_status[i][j] = 2;
		if flag=='x':
			utility, state= self.minimax(current_board,current_block_status, self.neg_inf, self.inf, True, 3, 1, 2, old_move)
		elif flag=='o':
			utility, state= self.minimax(current_board,current_block_status, self.neg_inf, self.inf, True, 3, 1, 2, old_move)
		# print utility
		return state[0],state[1]
		# for i in range(16):
		# 	for y in range(16):
		# 		# if(board.board_status[i][y]!=state.board_status[i][y]):
		# 			return statei,y

	def getvalid(self, current_board, current_block_status, old_move):
    		 #returns the valid cells allowed given the last move and the current board state
        	allowed_cells = []
        	allowed_block = [old_move[0] % 4, old_move[1] % 4]# checksif the move is a free move or not based on the rules

        	if old_move != (-1, -1) and current_block_status[allowed_block[0]][allowed_block[1]] == 0:
            		for i in range(4 * allowed_block[0], 4 * allowed_block[0] + 4):
                		for j in range(4 * allowed_block[1], 4 * allowed_block[1] + 4):
                    			if current_board[i][j] == 0:
                        			allowed_cells.append((i, j))
        	else :
            		for i in range(16):
                		for j in range(16):
                  		  	if current_board[i][j] == 0 and current_block_status[i / 4][j / 4] == 0:
                        			allowed_cells.append((i, j))
        	return allowed_cells


	def terminal_state(self, current_board, current_block_status):
        	final = self.update_block_status(current_block_status, (0, 0));
        	if final == 1:
            		return 1, 1000;
        	elif final == 2:
            		return 1, -1000;
	        elif final == 0:
	            return 0, 0;
        	elif final == 3:
            		var1=0;
            		var2=0;
            		for i in range(4):
                		for j in range(4):
                    			if current_block_status[i][j]==1 :
                        			var1=var1+1;
                    			elif current_block_status[i][j]==2:
                        			var1=var1-1;

            	if var1 > 0:
                	return 1,1000;
            	elif var1 < 0:
                	return 1,-1000;
            	var2=0;
            	for i in range(0,16,4):
                	for j in range(0,16,4):
                    		for z in range(1,3,1):
                        		for k in range(1,3,1):
                            			if current_board[i+z][j+k] ==1:
                            				    var2=var2+1;
                          			elif current_board[i+z][j+k]==2:
                                			    var2=var2-1;
            	if var2 > 0:
                	return 1,1000;
            	elif var2 < 0:
               		return 1,-1000;
            	else:
                	return 1,0;

	def update_block_status(self, curr_block, cell):
        	x = cell[0] / 4;
        	y = cell[1] / 4;
        	x = 4 * x;
        	y = 4 * y;
        	if curr_block[x + 0][y + 0] == curr_block[x + 1][y+1] == curr_block[x + 2][y + 2] == curr_block[x + 3][y + 3] and(curr_block[x + 0][y + 0] == 1 or curr_block[x + 0][y + 0] == 2):
            		return curr_block[x + 0][y + 0];
       		if curr_block[x + 0][y + 3] == curr_block[x + 1][y + 2] == curr_block[x + 2][y + 1] == curr_block[x + 3][y + 0] and(curr_block[x + 0][y + 3] == 1 or curr_block[x + 0][y + 3] == 2):
            		return curr_block[x + 0][y + 3];

        	for i in range(4):
            		if curr_block[x + i][y + 0] == curr_block[x + i][y + 1] == curr_block[x + i][y + 2] == curr_block[x + i][y + 3] and(curr_block[x + i][y + 0] == 1 or curr_block[x + i][y + 0] == 2):
                		return curr_block[x + i][y + 0];
        	for i in range(4):
            		if curr_block[x + 0][y + i] == curr_block[x + 1][y + i] == curr_block[x + 2][y + i] == curr_block[x + 3][y + i] and(curr_block[x + 0][y + i] == 1 or curr_block[x + 0][y + i] == 2):
                		return curr_block[x + 0][y + i];
        	flag = 0;
        	for i in range(4):
        	    for j in range(4):
                	if curr_block[i][j] != 0:
                	    flag = flag + 1;
       		if (flag == 16):
         	   return 3;
        	return 0;

	def hueristic(self, current_board, current_block_status, player_str, opponent_str):
	    	val = 0
	        # uttt= board.find_terminal_state()
		final, final_score = self.terminal_state(current_board, current_block_status);
	 	if final==1:
	            	if final_score > 1:
	                		return self.WIN_GAME_SCORE
	 		elif final_score<-1:
	            			return -self.WIN_GAME_SCORE
	        	if final_score==0:
	            		return self.TIE
	        for i in xrange(4):
	 		for y in range(4):
	            		 miniB_val = self.assess_miniB(current_board,current_block_status, i, y, player_str, opponent_str)
	             		 val += (self.CELL_WEIGHT[i][y] * miniB_val)
	        return val

	def assess_miniB(self, current_board,current_block_status, row, column, player_str, opponent_str):
	  	val = 0
	        if current_block_status[row][column]==player_str:
	 		return self.SUM_ALL_CELLS_WEIGHT
	 	if current_block_status[row][column]==opponent_str:
	                return -self.SUM_ALL_CELLS_WEIGHT
	        if current_block_status[row][column]=='3':
	            	return self.TIE
	        for i in xrange(4):
	 		for y in range(4):
	           			 if current_board[4*row+i][4*column+y] == 1:
	                			val += self.CELL_WEIGHT[i][y]
					 elif current_board[4*row+i][4*column+y] == 3:
	                			val += 0
	            			 else:
	                			val -= self.CELL_WEIGHT[i][y]
	 	return val


	# def is_block_full(self, state, row, column):
	#  	flag=0
	#  	for i in range(4):
	#  		for y in range(4):
	#  			if state.board_status[4*row+i][4*column+y]=='-':
	#  				flag=1
	#  	if flag==0:
	#  		return True
	#  	else:
	#  		return False
	# def hueristic(self, state, player_str, opponent_str):
	# 	uttt=state.find_terminal_state()
	# 	if uttt[1]=='WON':
	# 		free_cells=0
	# 		for i in range(4):
	# 			for y in range(4):
	# 				if(state.block_status[i][y]!='-'):
	# 					for a in range(4):
	# 						for b in range(4):
	# 							if state.board_status[4*i+a][4*y+b]=='-':
	# 								free_cells+=1
	# 		if uttt[0]==player_str:
	# 			return self.WIN_SCORE+free_cells
	# 		else:
	# 			return -self.WIN_SCORE-free_cells
	# 	if uttt[1]=='DRAW':
	# 		return 0
	# 	pl_count=0
	# 	op_count=0
	# 	filter_seq=[]
	# 	for seq in self.POSSIBLE_WIN_SEQUENCES:
	# 		for i in seq:
	# 			if state.block_status[i[0]][i[1]]!='-':
	# 						filter_seq.append(state.block_status[i[0]][i[1]])
	#         	if player_str in filter_seq:
    #             		if opponent_str in filter_seq:
    #                 			continue
    #             		if len(filter_seq) > 1:
    #                 			pl_count += self.APPROXIMATE_WIN_SCORE
    #             		pl_count += 1
    #             	elif opponent_str in filter_seq:
    #            			if len(filter_seq) > 1:
    #                 			op_count += self.APPROXIMATE_WIN_SCORE
    #             		op_count += 1
	# 		del filter_seq[0:len(filter_seq)]
    #     	ret=(pl_count-op_count)*self.BIG_BOARD_WEIGHT
	# 	for i in range(4):
	# 		for y in range(4):
	# 			if self.is_block_full(state,i,y)==False:
	# 				ret+=self.assess_miniB( state, i, y, player_str, opponent_str)
	# 	return ret
	#
	# def assess_miniB(self, state, row, column, player_str, opponent_str):
	# 	player_count=0
	# 	opponent_count=0
	# 	filtered_seq=[]
	# 	for seq in self.POSSIBLE_WIN_SEQUENCES:
	# 		for i in seq:
	# 			if state.board_status[4*row+i[0]][4*column+i[1]]!='-':
	# 						filtered_seq.append(state.board_status[4*row+i[0]][4*column+i[1]])
	#         	if player_str in filtered_seq:
    #             		if opponent_str in filtered_seq:
    #                 			continue
    #             		if len(filtered_seq) > 1:
    #                 			player_count += self.APPROXIMATE_WIN_SCORE
    #             		player_count += 1
    #             	elif opponent_str in filtered_seq:
    #            			if len(filtered_seq) > 1:
    #                 			opponent_count += self.APPROXIMATE_WIN_SCORE
    #             		opponent_count += 1
	# 		del filtered_seq[0:len(filtered_seq)]
    #     	return player_count - opponent_count



	def minimax(self,current_board,current_block_status, alpha, beta, maximizer, depth, maxp, minp, old_move):
		if depth==0:
			value =self.hueristic(current_board,current_block_status, maxp, minp)
			return value, ()
		moves = self.getvalid(current_board, current_block_status, old_move)
	    	if len(moves)==0:
	        	return self.hueristic(current_board,current_block_status, maxp, minp), ()
		random.shuffle(moves)
	    	if maximizer==True:
			utility=self.neg_inf
        		for i in moves:
            			tboard=copy.deepcopy(current_board)
            			tblock=copy.deepcopy(current_block_status)
            			tboard[i[0]][i[1]]=maxp
				tblock[i[0] / 4][i[1] / 4] = self.update_block_status(tboard, i);
            			Nutility,NState=self.minimax(tboard,tblock,alpha,beta,False,depth-1,maxp,minp,i)
            			if Nutility > utility:
                			utility=Nutility
                			returnState=i
				tboard[i[0]][i[1]] = 0;
                		tblock[i[0] / 4][i[1] / 4] = self.update_block_status(tboard, i);
				if utility>alpha:
					alpha=utility
            			if alpha >=beta :
					break;
			return utility,returnState

	    	else:
	        	utility=self.inf
	        	for i in moves:
	        	# 	nextState=copy.deepcopy(board)
	        	# 	nextState.board_status[i[0]][i[1]]=minp
				# k=(i[0],i[1])
				# nextState.update(old_move,k,minp)
				tboard=copy.deepcopy(current_board)
				tblock=copy.deepcopy(current_block_status)
				tboard[i[0]][i[1]]=minp
				tblock[i[0] / 4][i[1] / 4] = self.update_block_status(tboard, i);

				# old_move=(i[0],i[1])
	        		Nutility,Nstate=self.minimax(tboard,tblock,alpha,beta,True,depth-1,maxp,minp,i)
	        		if Nutility < utility:
	       	 	        	utility=Nutility
	        	        	returnState=i
				# nextState.board_status[i[0]][i[1]]='-'
				# nextState.update(k,old_move,'-')
				tboard[i[0]][i[1]] = 0;
                		tblock[i[0] / 4][i[1] / 4] = self.update_block_status(tboard, i);
				if utility< beta:
					beta=utility
	        	    	if alpha >=beta :
	        	        	break;
			return utility,returnState
