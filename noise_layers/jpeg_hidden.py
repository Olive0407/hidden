import torch
import torch.nn as nn
import numpy as np

class jpeg_redmark(nn.Module):
    """
    Drops random pixels from the noised image and substitues them with the pixels from the cover image
    """
    def __init__(self, keep_ratio_range):
        super(Dropout, self).__init__()
        self.keep_min = keep_ratio_range[0]
        self.keep_max = keep_ratio_range[1]


    def forward(self, noised_and_cover):

        noised_image = noised_and_cover[0]
        cover_image = noised_and_cover[1]

        mask_percent = np.random.uniform(self.keep_min, self.keep_max)
        #在01中随机挑选数字组成noised_image的shape，概率
        mask = np.random.choice([0.0, 1.0], noised_image.shape[2:], p=[1 - mask_percent, mask_percent])
        mask_tensor = torch.tensor(mask, device=noised_image.device, dtype=torch.float)
        # mask_tensor.unsqueeze_(0)
        # mask_tensor.unsqueeze_(0)
        mask_tensor = mask_tensor.expand_as(noised_image)
        noised_image = noised_image * mask_tensor + cover_image * (1-mask_tensor)
        return [noised_image, cover_image]


def qjpeg(self, x):
    # Q_flatten=Q_matrix.flatten()
    # Q_flatten=torch.from_numpy(Q_flatten)
    Q_flatten = Q_matrix.to(device).float()
    a = x.size()[2]
    b = x.size()[3]
    c = x.size()[0]
    for n in range(c):
        for i in range(a):
            for j in range(b):
                x[n, :, i, j] = ((x[n, :, i, j] * 255) / Q_flatten)
    y = self.add_gaussian_noise(x)
    for n in range(c):
        for i in range(a):
            for j in range(b):
                y[n, :, i, j] = (y[n, :, i, j] * Q_flatten / 255)
    return y