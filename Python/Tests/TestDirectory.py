import itk

d = itk.Directory.New()
d.Load(".")
n = d.GetNumberOfFiles()
i = 0
while i < n:
        print d.GetFile(i)
        i = i +1





