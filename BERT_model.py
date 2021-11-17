from transformers import pipeline
classifier = pipeline('sentiment-analysis')


output1 = classifier('Tesla is going to hell.')
output2 = classifier('Tesla is doing great.')

print(output1)
print(output2)