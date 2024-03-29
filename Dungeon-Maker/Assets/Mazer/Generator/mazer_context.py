import random
import clingo

class mazer_context:

    def __init__(self):
        self.memory=dict()

    def rand(self,offset,limit):
        lis = list()
        for i in range(0, limit.number + 1):
            lis += [random.randrange(offset.number,offset.number+ limit.number + 1)]
        #print(lis)
        rand_num = 0
        rand_num=lis[random.randrange(0,len(lis))]
        return clingo.Number(rand_num)

    def rand_center(self,x,dim,cor_val):
        nx=x.number
        ndim=dim.number
        ncor=cor_val.number
        half_cor=ncor//2
        half_dim=ndim//2
        rand_num=random.randrange(nx-half_dim+half_cor,nx+half_dim-half_cor)
        return clingo.Number(rand_num)

    def rand_size(self,x,min_val,max_val):
        nx=x.number
        rand_num=random.randrange(min_val.number,max_val.number+1)
        return clingo.Number((nx+rand_num*2)//3)

    def rand_dec(self,x,xsize,max_val):
        nval=x.number
        nmax=max_val.number
        rval=xsize.number
        rval_num=random.randrange(1,rval+1)
        rand_num=random.randrange(-nmax//2,nmax//2+1)
        return clingo.Number((nval+rand_num)%rval_num)

    def rand_point(self,max,distance):
        nmax=max.number
        ndist=distance.number
        lis=list(range(-nmax,nmax+1))
        rand_index=random.randrange(0,len(lis))
        return clingo.Number(lis[rand_index]*ndist)