from ..cb import CallBack 

class PSelect(CallBack):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.n = 0
        self.N = int(self.kwargs.get('N', 1)) # OPTIONAL
        self.P = list(self.kwargs.get('P', [f'P{i}' for i in range(self.N)])) # OPTIONAL
        assert len(self.P) == self.N

    def dip_state_handler(self, state):
        dip_state_dict = dict()
        for idxp, p in enumerate(self.P):
            extracted_point = state[idxp]
            F = self.kwargs.get('F', range(len(extracted_point))) # OPTIONAL
            for idxf, f in enumerate(extracted_point):
                dip_state_dict[f'{p}_{F[idxf]}'] = f
        return dip_state_dict
    
    def CB_EVENT_LBUTTONDOWN(self, **kwargs):
        """
            # NOTE: you can overwrite this function for new inherited PSelect class, i.e. for extracting other features than x,y.
        """
        if self.n < self.N:
            self.n += 1
            self.winupdate(center=[kwargs['x'], kwargs['y']])
            self.state.append([kwargs['x'], kwargs['y']]) # NOTE: overwritable candidate => feature extraction

        if self.n >= self.N:
            self.winclose()
    
if __name__ == '__main__':
    # TEST 0
    from ..processing.sharpening import Basic as BasicSharpener
    basicsharpener = BasicSharpener(
        SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        SPATH_HEAD=3,
        DF_DPATH='*/RetinaLessions.csv',
        CALLBACK=PSelect,
        CALLBACK_ARGS=dict(N=2, F=['X', 'Y'], P=['OD', 'FOV'])
    )
    print(basicsharpener.df)