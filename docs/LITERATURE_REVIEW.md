# Literature review notes: hippocampal pattern separation and completion

**Status:** Working source map, not a systematic review.  
**Purpose:** Keep empirical findings, computational interpretations, and framework design choices distinct.  
**Last reviewed:** 2026-11-28

## Scope and terminology

Pattern separation and pattern completion are useful computational descriptions of transformations associated with episodic memory. They should not be treated as interchangeable with any one neural metric or behavioural task. Studies operationalize them differently across species, hippocampal subfields, tasks, and measurement methods.

For this project:

- **Pattern separation (computational target):** a transformation that makes representations of overlapping inputs more distinguishable, evaluated while accounting for information retained.
- **Pattern completion (computational target):** recovery of target information or a stored representation from a partial or degraded cue.
- **Mnemonic discrimination:** a behavioural ability to distinguish highly similar experiences or lures; it is related to, but not identical with, a direct measurement of a neural pattern-separation transformation.
- **Nearest-neighbour selection:** choosing an existing stored item by a distance rule. This is not reconstruction and is not sufficient evidence of pattern completion.

These are working operational distinctions for MM. They are not claims that the biological constructs have universally agreed definitions.

## Selected sources and what they support

### 1. Complementary learning systems

McClelland, J. L., McNaughton, B. L., & O'Reilly, R. C. (1995). Why there are complementary learning systems in the hippocampus and neocortex: Insights from the successes and failures of connectionist models of learning and memory. *Psychological Review, 102*(3), 419–457. https://doi.org/10.1037/0033-295X.102.3.419

- **Source type:** computational/theoretical paper.
- **Use in manuscript:** historical and theoretical motivation for complementary learning systems.
- **Caution:** this is a theory paper, not direct empirical validation of the current binary framework.

### 2. Dentate gyrus and CA3 population representations

Leutgeb, J. K., Leutgeb, S., Moser, M.-B., & Moser, E. I. (2007). Pattern separation in the dentate gyrus and CA3 of the hippocampus. *Science, 315*(5814), 961–966. https://doi.org/10.1126/science.1135801

- **Source type:** primary electrophysiological research in rats.
- **Finding relevant to MM:** small environmental changes altered correlated activity among dentate-gyrus granule cells; larger environmental changes recruited new CA3 cell populations.
- **Interpretive caution:** the findings support a nuanced account in which separation-related changes may involve both DG and CA3, not a simplistic one-region/one-operation mapping.

### 3. Human high-resolution fMRI

Bakker, A., Kirwan, C. B., Miller, M., & Stark, C. E. L. (2008). Pattern separation in the human hippocampal CA3 and dentate gyrus. *Science, 319*(5870), 1640–1642. https://doi.org/10.1126/science.1152882

- **Source type:** primary human neuroimaging study.
- **Finding relevant to MM:** activity in the combined CA3/DG region was consistent with a bias toward pattern separation during the study's mnemonic discrimination paradigm.
- **Interpretive caution:** the study does not functionally distinguish CA3 from DG; the result is a regional fMRI signal, not a direct measurement of individual-neuron transformations.

### 4. CA3 response to degraded/conflicting cues

Neunuebel, J. P., & Knierim, J. J. (2014). CA3 retrieves coherent representations from degraded input: Direct evidence for CA3 pattern completion and dentate gyrus pattern separation. *Neuron, 81*(2), 416–427. https://doi.org/10.1016/j.neuron.2013.11.017

- **Source type:** primary simultaneous electrophysiological recordings in behaving rats.
- **Finding relevant to MM:** during local/global reference-frame conflict, DG population representations were disrupted while CA3 responses were more coherent with the stored environmental representation.
- **Interpretive caution:** the result is tied to a particular spatial task and neural measurement; it does not imply that every CA3 process is completion or that a generic nearest-neighbour algorithm models CA3.

### 5. Cross-method and cross-species caveats

Yassa, M. A., & Stark, C. E. L. (2011). Pattern separation in the hippocampus. *Trends in Neurosciences, 34*(10), 515–525. https://doi.org/10.1016/j.tins.2011.06.006

- **Source type:** review.
- **Use in manuscript:** methodological cautions across electrophysiology, lesion studies, immediate-early gene methods, animal models, and human fMRI.
- **Cautions highlighted:** limitations in separating CA3 from DG with human fMRI; sensory manipulations are imperfect proxies for upstream neural input; the relation between subfield signals and behavioural output is not straightforward.
- **Use:** cite as a review for limitations, not as a primary experiment.

### 6. Temporal pattern separation in hippocampal neurons

Madar, A. D., Ewell, L. A., & Jones, M. V. (2019). Pattern separation of spiketrains in hippocampal neurons. *Scientific Reports, 9*, 5282. https://doi.org/10.1038/s41598-019-41503-8

- **Source type:** primary experimental study using mouse hippocampal slices, with computational analyses.
- **Finding relevant to MM:** granule-cell output spike trains were more dissimilar than their input spike trains under the tested stimulation conditions.
- **Interpretive caution:** this concerns temporal spike-train representations in an ex vivo preparation; it is not equivalent to the static binary-vector task currently implemented in MM.

## Implications for MM design

1. A binary-vector similarity change is a software-level representation result. It is not a direct measure of hippocampal neural activity.
2. A sparsity constraint or lower output overlap does not establish information preservation. MM must measure recoverability or decoding performance separately.
3. The DG/CA3 literature motivates multiple computational roles but does not justify calling random projection, k-WTA, or hashing biologically faithful DG models.
4. Pattern completion requires a reconstruction or target-recovery outcome. Returning the closest stored ID is only a selection baseline.
5. MM's missing-feature and substitution cues are controlled mathematical perturbations. They are not claimed to reproduce any specific sensory, neural, or clinical degradation process.
6. Findings from human fMRI, rodent electrophysiology, ex vivo slices, and computational models must be described according to their methods and cannot be pooled as if they were the same measurement.

## Open literature tasks

- Read full texts and verify every manuscript claim against the exact methods and results sections.
- Add classic computational models of DG sparse coding and CA3 autoassociation, including Marr's archicortex theory and later formal models, with clear distinction between theory and empirical evidence.
- Review mnemonic discrimination task validity and its relation to neural pattern separation.
- Identify appropriate representational similarity and decoding methods for MM's binary setting.
- Search for counterevidence, alternative interpretations, and studies showing condition-dependent DG/CA3 computations before making broad generalizations.

## Source links

- [McClelland et al. (1995), DOI](https://doi.org/10.1037/0033-295X.102.3.419)
- [Leutgeb et al. (2007), PubMed](https://pubmed.ncbi.nlm.nih.gov/17303747/)
- [Bakker et al. (2008), PubMed](https://pubmed.ncbi.nlm.nih.gov/18356518/)
- [Neunuebel & Knierim (2014), PubMed](https://pubmed.ncbi.nlm.nih.gov/24462102/)
- [Yassa & Stark (2011), PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC3183227/)
- [Madar et al. (2019), PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC6437159/)
