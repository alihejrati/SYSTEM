# DELETE: this file is not used and you can delete it.

import torch
from torch.nn import functional as F
from KERNEL.PYTHON.classes.basic import PYBASE

class Patcher(PYBASE):
    """
        # TODO: now we only impliment 2d functions you can see this link and copy 3d and 4d functions as will.
        *https://stackoverflow.com/questions/68150248/how-to-extract-overlapping-patches-from-a-3d-volume-and-recreate-the-input-shape


        *Note that if you have overlapping patches and you combine them, the overlapping elements will be summed. If you would like to get the initial input again there is a way:
            Create similar sized tensor of ones as the patches with torch.ones_like(patches_tensor).
            Combine the patches into full tensor with same output shape. (this creates a counter for overlapping elements).
            Divide the Combined tensor with the Combined ones, this should reverse any double summation of elements.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass
    
    def get_dim_blocks_2d(self, dim_in, dim_kernel_size, dim_padding = 0, dim_stride = 1, dim_dilation = 1):
        dim_out = (dim_in + 2 * dim_padding - dim_dilation * (dim_kernel_size - 1) - 1) // dim_stride + 1
        return dim_out

    def extract_patches_2ds(self, x, kernel_size, padding=0, stride=1):
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        if isinstance(padding, int):
            padding = (padding, padding, padding, padding)
        if isinstance(stride, int):
            stride = (stride, stride)

        channels = x.shape[1]

        x = torch.nn.functional.pad(x, padding)
        # (B, C, H, W)
        x = x.unfold(2, kernel_size[0], stride[0]).unfold(3, kernel_size[1], stride[1])
        # (B, C, h_dim_out, w_dim_out, kernel_size[0], kernel_size[1])
        x = x.contiguous().view(-1, channels, kernel_size[0], kernel_size[1])
        # (B * h_dim_out * w_dim_out, C, kernel_size[0], kernel_size[1])
        return x

    def extract_patches_2d(self, x, **kwargs):
        kernel_size = int(kwargs.get('k', 4))
        stride = int(kwargs.get('s', 1))
        padding = int(kwargs.get('p', 0))
        dilation = int(kwargs.get('d', 1))
        
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        if isinstance(padding, int):
            padding = (padding, padding)
        if isinstance(stride, int):
            stride = (stride, stride)
        if isinstance(dilation, int):
            dilation = (dilation, dilation)

        NOT_USED, channels, h_dim_in, w_dim_in = x.shape
        h_dim_out = self.get_dim_blocks_2d(h_dim_in, kernel_size[0], padding[0], stride[0], dilation[0])
        w_dim_out = self.get_dim_blocks_2d(w_dim_in, kernel_size[1], padding[1], stride[1], dilation[1])

        # (B, C, H, W)
        x = F.unfold(x, kernel_size, padding=padding, stride=stride, dilation=dilation)
        # (B, C * kernel_size[0] * kernel_size[1], h_dim_out * w_dim_out)
        x = x.view(-1, channels, kernel_size[0], kernel_size[1], h_dim_out, w_dim_out)
        # (B, C, kernel_size[0], kernel_size[1], h_dim_out, w_dim_out)
        x = x.permute(0,1,4,5,2,3)
        # (B, C, h_dim_out, w_dim_out, kernel_size[0], kernel_size[1])
        x = x.contiguous().view(-1, channels, kernel_size[0], kernel_size[1])
        # (B * h_dim_out * w_dim_out, C, kernel_size[0], kernel_size[1])
        return x

    def combine_patches_2d(self, x, kernel_size, output_shape, padding=0, stride=1, dilation=1):
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        if isinstance(padding, int):
            padding = (padding, padding)
        if isinstance(stride, int):
            stride = (stride, stride)
        if isinstance(dilation, int):
            dilation = (dilation, dilation)

        def get_dim_blocks(dim_in, dim_kernel_size, dim_padding = 0, dim_stride = 1, dim_dilation = 1):
            dim_out = (dim_in + 2 * dim_padding - dim_dilation * (dim_kernel_size - 1) - 1) // dim_stride + 1
            return dim_out

        channels = x.shape[1]
        h_dim_out, w_dim_out = output_shape[2:]
        h_dim_in = get_dim_blocks(h_dim_out, kernel_size[0], padding[0], stride[0], dilation[0])
        w_dim_in = get_dim_blocks(w_dim_out, kernel_size[1], padding[1], stride[1], dilation[1])

        # (B * h_dim_in * w_dim_in, C, kernel_size[0], kernel_size[1])
        x = x.view(-1, channels, h_dim_in, w_dim_in, kernel_size[0], kernel_size[1])
        # (B, C, h_dim_in, w_dim_in, kernel_size[0], kernel_size[1])
        x = x.permute(0,1,4,5,2,3)
        # (B, C, kernel_size[0], kernel_size[1], h_dim_in, w_dim_in)
        x = x.contiguous().view(-1, channels * kernel_size[0] * kernel_size[1], h_dim_in * w_dim_in)
        # (B, C * kernel_size[0] * kernel_size[1], h_dim_in * w_dim_in)
        x = torch.nn.functional.fold(x, (h_dim_out, w_dim_out), kernel_size=(kernel_size[0], kernel_size[1]), padding=padding, stride=stride, dilation=dilation)
        # (B, C, H, W)
        return x






if __name__ == '__main__':
    from DATA.OPENCV.basic import load as cvload, imshow as cvimshow
    patcher = Patcher()

    # TEST 0) First (2D):
    # offitial test:
    # a = torch.arange(1, 65, dtype=torch.float).view(2,2,4,4)
    # print(a.shape)
    # print(a)
    # b = patcher.extract_patches_2d(a, 2, padding=1, stride=2, dilation=1)
    # # b = extract_patches_2ds(a, 2, padding=1, stride=2)
    # print(b.shape)
    # print(b)
    # c = patcher.combine_patches_2d(b, 2, (2,2,4,4), padding=1, stride=2, dilation=1)
    # print(c.shape)
    # print(c)
    # print(torch.all(a==c))

    # my test:
    x = torch.randint(0,256, (2,3,256,256), dtype=torch.float32, requires_grad=True)
    y = patcher.extract_patches_2d(x)
    print(y.shape)
    # TODO: test on batch of images.
    # img = cvload('*/lena.jpg')
    # print(img.shape)
    # x = torch.tensor(cvload('*/lena.jpg'))

    