from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Input, Lambda, Layer
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD, RMSprop
from keras.models import load_model
from keras import backend as K
from keras import metrics
from keras.initializers import glorot_uniform

encoder = None
generator = None

epsilon_std = 1.0
latent_dim = 2
batch_size = 100

seed = 1
glorot = glorot_uniform(seed)

def sampling(args):
    z_mean, z_log_var = args
    # epsilon = K.random_normal(shape=(batch_size, latent_dim), mean=0.,
    #                           stddev=epsilon_std)
    epsilon = K.random_normal(shape=(latent_dim,), mean=0.,
                              stddev=epsilon_std)
    return z_mean + K.exp(z_log_var / 2) * epsilon


def declare_model(input_dim, intermediate_dim, latent_dim):

    x = Input(shape=(input_dim,), name="input")
    #x3 = Dense(intermediate_dim * 4, activation='relu', name="h3")(x)
    #x2 = Dense(intermediate_dim * 2, activation='relu', name="h2")(x)
    h = Dense(intermediate_dim, activation='relu', kernel_initializer=glorot, name="h")(x)
    z_mean = Dense(latent_dim, activation='relu', kernel_initializer=glorot, name="z-mean")(h)
    z_log_var = Dense(latent_dim, activation='relu', kernel_initializer=glorot, name="z-log-var")(h)

    # def sampling(args):
    #     z_mean, z_log_var = args
    #     epsilon = K.random_normal(shape=(batch_size, latent_dim), mean=0.,
    #                               stddev=epsilon_std)
    #     return z_mean + K.benchmarks(z_log_var / 2) * epsilon

    # note that "output_shape" isn't necessary with the TensorFlow backend
    z = Lambda(sampling, output_shape=(latent_dim,), name="z")([z_mean, z_log_var])

    # we instantiate these layers separately so as to reuse them later
    decoder_x3 = Dense(intermediate_dim * 4, activation='relu', kernel_initializer=glorot, name="decoder_x3")
    decoder_x2 = Dense(intermediate_dim * 2, activation='relu', kernel_initializer=glorot, name="decoder_x2")
    decoder_h = Dense(intermediate_dim, activation='relu', kernel_initializer=glorot, name="decoder_h")
    decoder_mean = Dense(input_dim, activation='sigmoid', name="decoder_z_mean")
    h_decoded = decoder_h(z)
    #x2_decoded = decoder_x2(h_decoded)
    #x3_decoded = decoder_x3(x2_decoded)
    x_decoded_mean = decoder_mean(h_decoded)

    class CustomVariationalLayer(Layer):
        def __init__(self, **kwargs):
            self.is_placeholder = True
            self.beta = 1
            super(CustomVariationalLayer, self).__init__(**kwargs)

        def vae_loss(self, x, x_decoded_mean):
            #xent_loss = input_dim * metrics.binary_crossentropy(x, x_decoded_mean)
            #xent_loss = metrics.binary_crossentropy(x, x_decoded_mean)
            xent_loss = metrics.mean_squared_error(x, x_decoded_mean)
            kl_loss = self.beta * (- 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1))
            return K.mean(xent_loss + kl_loss)

        def call(self, inputs):
            x = inputs[0]
            x_decoded_mean = inputs[1]
            loss = self.vae_loss(x, x_decoded_mean)
            self.add_loss(loss, inputs=inputs)
            # We won't actually use the output.
            return x

    y = CustomVariationalLayer(name="variational_layer")([x, x_decoded_mean])
    vae = Model(x, y)

    # Code input into latent space
    global encoder
    encoder = Model(x, z_mean, name="encoder")

    # Sample from latent space
    decoder_input = Input(shape=(latent_dim,), name="decoder_input")
    _h_decoded = decoder_h(decoder_input)
    #_x2_decoded = decoder_x2(_h_decoded)
    #_x3_decoded = decoder_x3(_x2_decoded)
    _x_decoded_mean = decoder_mean(_h_decoded)

    global generator
    generator = Model(decoder_input, _x_decoded_mean, name="generator")

    return vae

# def vae_loss(x, x_decoded_mean):
#     #x = K.flatten(x)
#     xent_loss = original_dim * metrics.binary_crossentropy(x, x_decoded_mean)
#     kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.benchmarks(z_log_var), axis=-1)
#     return K.mean(xent_loss + kl_loss)


def compile_model(model):
    #sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    #rms = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
    model.compile(optimizer='adadelta', loss=None)
    #model.compile(optimizer=sgd, loss=None)
    return model


def train_model(model, x, epochs=10, batch_size=256):
    model.fit(x, x, epochs=epochs, batch_size=batch_size, shuffle=True)
    #model.train_on_batch(x, x)
    return model


def train_model_incremental(model, input_gen, epochs=20, steps_per_epoch=512, callbacks=None):
    model.fit_generator(input_gen, epochs=epochs, steps_per_epoch=steps_per_epoch, callbacks=callbacks)
    return model


def evaluate_model(model, x):
    score = model.evaluate(x, x, batch_size=128)
    return score


def evaluate_model_incremental(model, input_gen, steps=1000):
    score = model.evaluate_generator(input_gen, steps)
    return score


def encode_input(input):
    encoded_input = encoder.predict(input)
    return encoded_input


def decode_input(input):
    decoded_input = generator.predict(input)
    return decoded_input


def save_model_to_path(model, path):
    model.save(path + "vae.h5")
    if encoder is not None:
        encoder.save(path + "vae_encoder.h5")
    if generator is not None:
        generator.save(path + "vae_generator.h5")


def load_model_from_path(path):
    model = load_model(path)
    return model

if __name__ == "__main__":
    print("Basic autoencoder")

    # evaluator coding/decoding

    from preprocessing.utils_pre import binary_encode, binary_decode

    integerl = [0, 0, 43, 938458, 1]
    print(str(integerl))
    bincode = binary_encode(integerl)
    print(str(bincode))
    intcode = binary_decode(bincode)
    print(str(intcode))


    exit()


    from sklearn.datasets import fetch_20newsgroups
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer

    categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(twenty_train.data)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    dim = X_train_tfidf.shape[1]

    samples = X_train_tfidf.shape[0]

    def input_gen(batch_size):
        while True:
            batch = []
            size = 0
            for i in range(X_train_tfidf.shape[0]):
                dense_array = X_train_tfidf[i].todense()
                batch.append(dense_array)
                size += 1
                if size == batch_size:
                    yield dense_array, dense_array
                    dense_array = []
                    size = 0


    ae = declare_model(dim, 128)
    ae = compile_model(ae)

    #ae = train_model(ae, X_train_tfidf)

    ae = train_model_incremental(ae, input_gen(32), epochs=10, steps_per_epoch=(samples/32)-1)

    save_model_to_path(ae, "test_ae.h5")
