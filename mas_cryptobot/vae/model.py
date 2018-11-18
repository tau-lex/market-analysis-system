from mas_tools.models.autoencoders import deep_conv2d_vae
from mas_tools.ml import save_model_arch


if __name__ == "__main__":
    path = 'E:/Projects/market-analysis-system/mas_vae/'

    enc, dec, ae, _ = deep_conv2d_vae((80, 80, 3), latent_dim=60, filters_count=(3, 15), dropout=0.3)
    save_model_arch(enc, path+'ae_enc')
    enc.summary()
    save_model_arch(dec, path+'ae_dec')
    dec.summary()
    save_model_arch(ae, path+'ae')
    ae.summary()
