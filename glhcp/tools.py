import os
from pathlib import Path
from warnings import warn

def _input_checks_meg(subject,
                hcp_path,
                freq_band,
                source,
                subjects_dir,
                parc,
                snr,
                saving_dir,
                create_report,
                ):
    """
    Checking inputs before starting the analysis.
    """

    if not isinstance(subject, str):
        raise TypeError(f"subject must be string got type {type(subject).__name__} instead.")
    
    if not isinstance(hcp_path, (str, Path)):
        raise TypeError(f"Expected str or Path, got {type(hcp_path).__name__} for hcp_path.")
    hcp_path = Path(hcp_path)

    freq_bands = {
                "delta": [0.5, 4],
                "theta": [4, 8],
                "alpha": [8, 13],
                "beta": [13, 30],
                "gamma": [30, 80]
                }
    if freq_band in freq_bands:
        freqs = freq_bands[freq_band]
    if isinstance(freq_band, tuple) and len(freq_band) == 2 and freq_band[0] < freq_band[1]:
        freqs = freq_band
    else:
        raise TypeError(f"freq_band must be either one of {list(freq_bands.keys())} or tuple with two elements.")
    
    ## freq_band should be list of tuples or strings

    if not isinstance(source, bool):
        raise TypeError(f"source must be boolean, got type {type(source).__name__} instead.")
    
    if not (isinstance(subjects_dir, (str, Path)) or subjects_dir is None):
        raise TypeError(f"Expected str or Path or None, got {type(subjects_dir).__name__} for hcp_path.")
    if subjects_dir is None:
        subjects_dir = hcp_path / "subjects"
    else:
        subjects_dir = Path(subjects_dir)
        
    if not isinstance(parc, (str, list)):
        raise TypeError(f"parc must be string or list, got type {type(parc).__name__} instead.")
    
    if isinstance(parc, str): parc = [parc]
    label_folder = subjects_dir / subject / "label"
    label_fnames = os.listdir(label_folder)
    for par in parc:
        for hemi in ["lh", "rh"]:
            if f"{hemi}.{par}.annot" not in label_fnames:
                raise ValueError(f"{hemi}.{par}.annot not found in the {label_folder}")
        
    if not isinstance(snr, float): raise TypeError(f"snr must be float, got type {type(snr).__name__} instead.")
    if snr != 1.0:
        warn(f"Usually for raw MEG recordings snr of 1.0 is a safe choice. \
            see (https://mne.tools/stable/auto_examples/inverse/compute_mne_inverse_raw_in_label.html) \
            for more information.")
    
    if not (isinstance(saving_dir, (str, Path)) or saving_dir is None):
            raise TypeError(f"Expected str or Path or None, got {type(saving_dir).__name__} for hcp_path.")
    if saving_dir is None:
        saving_dir = hcp_path / "activations"
    else:
        saving_dir = Path(saving_dir)
    
    if not isinstance(create_report, bool):
        raise TypeError(f"source must be boolean, got type {type(create_report).__name__} instead.")
    
    return hcp_path, subjects_dir, freqs, parc, saving_dir