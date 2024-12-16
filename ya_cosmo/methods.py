import pygame


def scale_images(coefs, *args):
    """Апскейл изображений под разрешение экрана."""
    scale = coefs

    list_images = []

    for image in args:
        if isinstance(image, list):
            new_images = []
            for sprite in image:
                rect = sprite.get_rect()
                rect.width = rect.width // scale
                rect.height = rect.height // scale
                sprite = pygame.transform.scale(sprite,
                                                (rect.width,
                                                 rect.height))

                new_images.append(sprite)
            list_images.append(new_images)
        else:
            rect = image.get_rect()
            rect.width = rect.width // scale
            rect.height = rect.height // scale
            image = pygame.transform.scale(image,
                                           (rect.width,
                                            rect.height))
            list_images.append(image)

    if len(list_images) > 1:
        return list_images

    return list_images[0]
