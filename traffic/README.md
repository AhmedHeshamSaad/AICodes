The best trial was while using more convulotion layers. Convulotion layer is conputationally expensive without using Maxpooling filter. On the other hand, maxpooling layer reduces the model accuracy. The best accuracy I get when using 2 convolution layes before maxpooling the image. The trials are listed as follows.

first trial:
    Sequential model:
    numbers of convolutional and pooling layers: 1
    numbers and sizes of filters for convolutional layers: 32
    pool sizes for pooling layers: (2,2)
    numbers x sizes of hidden layers: 1x128
    dropout: 0.5
    results: 333/333 - 2s - loss: 1.1926 - accuracy: 0.6349

2nd trial:
    numbers x sizes of hidden layers: 1x128 + 1x128
    333/333 - 2s - loss: 3.5060 - accuracy: 0.0537

3rd trial:
    numbers x sizes of hidden layers: 1x128
    dropout: 0.3
    333/333 - 2s - loss: 1.7018 - accuracy: 0.4819

4th trial:
    numbers of convolutional and pooling layers: conv-maxpool-conv-maxpool
    dropout: 0.5
    333/333 - 4s - loss: 0.3290 - accuracy: 0.9101

5th trial:
    numbers of convolutional and pooling layers: conv-conv-maxpool
    333/333 - 7s - loss: 0.1177 - accuracy: 0.9759

6th trial:
    numbers of convolutional and pooling layers: conv-maxpool-conv-maxpool-conv-maxpool
    333/333 - 2s - loss: 0.3429 - accuracy: 0.9117

7th trial:
    numbers of convolutional and pooling layers: conv-maxpool-conv-conv-maxpool
    333/333 - 4s - loss: 0.1145 - accuracy: 0.9716

8th trial:
    numbers of convolutional and pooling layers: conv-conv-maxpool-conv-maxpool
    333/333 - 7s - loss: 0.0872 - accuracy: 0.9802
