# Pensieve

A neural network and API for recognizing objects in images.

This project implements Pylearn2 trained on the ImageNet database. The
API accepts either:
* A link to an image, or
* A buzzid

and returns the list of objects that it recognizes in the image or buzz.

As a proof of concept, we're starting with cats and dogs.  The collection
of objects will be expanded over time as we train the neural networks on
more types of images.
