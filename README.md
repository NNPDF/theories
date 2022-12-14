# Grid theory repository
Contains all ingredientes (grid, operator card, dataset definition) necessary to regenerate any theory using the pineko structure.

This can be read off `pineko.toml`.

Grids are in `data/grids/<theory>/`
Operator cards are in `data/operator_cards/<theory>`
Dataset definition is in `data/yamldb/<theory>`.

Note that `pineko` uses only one source of `yamldb` files since in principle these are theory independent. However, to help reproducibility (and to track any changes) they will be stored separately.

The folder `misc/<theory>` contain relevant checks and tests.
