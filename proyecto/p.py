from skimage.morphology import skeletonize
from skimage import io
from scipy import misc
from skimage.util import invert


def skeleton():
    image = io.imread('p.png', 1)
    # Invert the horse image
    image = invert(image)
    for b, f in enumerate(image):
        for a, p in enumerate(f):
            image[b][a] = 0 if image[b][a] == 255 else 1
    # perform skeletonization
    skeleton = skeletonize(image)
    misc.imsave('lena.png', skeleton)
    return skeleton


def displayResults():
    # display results
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                             sharex=True, sharey=True,
                             subplot_kw={'adjustable': 'box-forced'})
    ax = axes.ravel()
    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].axis('off')
    ax[0].set_title('original', fontsize=20)

    ax[1].imshow(skeleton, cmap=plt.cm.gray)
    ax[1].axis('off')
    ax[1].set_title('skeleton', fontsize=20)

    fig.tight_layout()
    plt.show()
