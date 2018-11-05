import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot

def plot_stat_comparison(title, A, labelA, B, labelB, S, startTime, timeStep):
    assert(len(A) == len(B) and len(B) == len(S))
    f = pyplot.figure()
    pyplot.title(title)

    xmin = startTime
    xmax = startTime + timeStep * (len(A) - 1)
    times = range(xmin, xmax + timeStep, timeStep)
    pyplot.xlim(xmin, xmax)

    for x in range(0, len(A)):
        if S[x]:
            if A[x] > B[x]:
                color = "#2eff00"
            else:
                color = "#ff1100"
            tl = times[x] - timeStep / 2
            tc = times[x]
            tr = times[x] + timeStep / 2
            ac = A[x]
            bc = B[x]
            if x < len(A) - 1:
                ar = (A[x] + A[x+1])/2
                br = (B[x] + B[x+1])/2
                pyplot.fill([tc, tr, tr, tc], [ac, ar, br, bc], color, linewidth=0)
            if x > 0:
                al = (A[x-1] + A[x])/2
                bl = (B[x-1] + B[x])/2
                pyplot.fill([tl, tc, tc, tl], [al, ac, bc, bl], color, linewidth=0)

    pyplot.plot(times, A, color = "#198800", label = labelA)
    pyplot.plot(times, B, color = "#b90c00", label = labelB)
    pyplot.plot(times, A-B, color = "#000099")

    pyplot.grid()
    pyplot.axvline(0, color="#888888")
    pyplot.axhline(0, color="#888888")

    pyplot.xlabel("time")
    pyplot.ylabel("avg. amplitude")
    pyplot.legend(loc = "upper right", framealpha = 0.5)

    return f
