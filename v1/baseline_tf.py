import tensorflow as tf
import numpy as np
from v1.tools import *
import random

# Define the model we'll use
class Warfarin:
  def __init__(self, inputs, outputs):
    # Create placeholders
    self.x = tf.placeholder(shape=[None, inputs], dtype=tf.float32)  # assuming a float input in [0, 1]
    self.y = tf.placeholder(shape=[None], dtype=tf.int64)

    # Define a fully-connected network with two hidden layers
    out = self.x
    out = tf.layers.dense(out, units=32, activation=tf.nn.relu)
    out = tf.layers.dense(out, units=32, activation=tf.nn.relu)
    out = tf.layers.dense(out, units=32, activation=tf.nn.relu)
    out = tf.layers.dense(out, units=outputs, activation=None)

    # Compute loss and accuracy
    self.preds = tf.argmax(out, axis=1)
    self.accuracy = tf.reduce_mean(tf.cast(tf.equal(self.preds, self.y), tf.float32))
    self.loss = tf.losses.sparse_softmax_cross_entropy(self.y, out)

def get_x(arr):
  return np.array([[r["age"], r["height"], r["weight"], r["race_asian"],
                    r["race_black"], r["race_missing"], r["enzyme"],
                    r["amiodarone"], r["male"], r["aspirin"]] for r in arr])

def get_y(arr):
  return np.array([int(r["label"]) for r in arr])

if __name__ == '__main__':
  data = load_dataset_clinical()
  random.shuffle(data)

  train_count = int(len(data) * 0.75)
  train = data[:train_count]
  test = data[train_count:]

  x_train = get_x(train)
  y_train = get_y(train)

  x_test = get_x(test)
  y_test = get_y(test)

  print('Loaded {} training, {} test examples'.format(len(x_train), len(x_test)))

  # Create the model and optimizer
  model = Warfarin(10, 3)
  optimizer = tf.train.AdamOptimizer(0.001)
  train_op = optimizer.minimize(model.loss)
  init_op = tf.global_variables_initializer()

  # For Tensorboard logging
  tf.summary.scalar('train_loss', model.loss)
  tf.summary.scalar('train_acc', model.accuracy)
  summary_op = tf.summary.merge_all()

  with tf.Session() as sess:
    # Initializes variables in the graph
    sess.run(init_op)

    # Create a summary writer
    writer = tf.summary.FileWriter('./logs/model', graph=tf.get_default_graph())

    # Main training loop
    for step in range(1000):
      # Create a mini-batch
      indices = np.random.permutation(len(x_train))[:1000]
      x_batch = x_train[indices]
      y_batch = y_train[indices]

      _, loss, accuracy, summary = sess.run(
          [train_op, model.loss, model.accuracy, summary_op],
          feed_dict={model.x: x_batch, model.y: y_batch})

      if step % 5 == 0:
        writer.add_summary(summary, step)

      if step % 50 == 0:
        print('Step: {}, loss: {}, accuracy: {}'.format(step, loss, accuracy))

    print('Training complete!')

    # Evaluate performance on the test set
    test_loss, test_accuracy = sess.run(
        [model.loss, model.accuracy],
        feed_dict={model.x: x_test, model.y: y_test})

    print('Test loss: {}, accuracy: {}'.format(test_loss, test_accuracy))