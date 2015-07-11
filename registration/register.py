__author__ = 'james'


def register(model, sample):

    # Globally align
    global_alignment(model, sample)

    # Articulated registration
    articulated_registration(model, sample)

    return model

def global_alignment(model, sample):
    pass

def articulated_registration(model, sample):
    pass


