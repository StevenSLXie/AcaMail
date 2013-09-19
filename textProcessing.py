from pyx import *
import numpy as np
import matplotlib.pyplot as plt



left, width = .25, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

def plotText():
	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')
	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	ax.text(left, bottom, r"$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!",horizontalalignment='left',verticalalignment='top',transform=ax.transAxes)
	ax.text(left, bottom,r"$\displaystyle\sum_{n=3}^\infty\frac{-e^{i\pi}}{4^n}$!", horizontalalignment='left',verticalalignment='bottom', transform=ax.transAxes)
	ax.text(0,0.8,'fdsfhdk\nshfjjjjjjjjjjjjj\neuwyrieywdsf\niryeiyreywyr\newryeyrieyryewyri\neyreuyrieyr\niyewiriweurojflkdjflsdfljdsifoueiryeyreuroweuroueworeowirueoiwurweiuruoeufhjkdhfjkdhhkj')
	ax.set_axis_off()
#	plt.show()
	plt.savefig('/Users/xingmanjie/Applications/Research/AcaMail/demo')


# textSort() sort out the body of the email, identifying those 'plain text' and display as it is. For those Tex, create a .png for each Tex. a Tex starts with a '$' and ends with the same symbol.
def textSort(body):
	math = []
	nonMath = []
	lastEnd = -1
	lastStart = 0
	i = 0
	j = 0
	while i < len(body):
		print i
		if body[i] == '$':
			nonMath.append(body[lastEnd+1:i])
			lastStart = i
			for j in range(len(body[i+1:])):
#	print i,j,len(body)
				if body[i+j+1]== '$':
					lastEnd = i+j+1
					math.append(body[i:lastEnd+1])
					i = i+j+1
					break
			i = i+1
		else:
			i = i+1

		j = 0
	if lastEnd != len(body)-1:
		nonMath.append(body[lastEnd+1:])


	return math,nonMath


def test():
	testString = 'This is a test string. Below is the formula:$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$ Of course, there are other formulae: $\left(\frac{5 - \frac{1}{x}}{4}\right)$'
	print textSort(testString)
			


