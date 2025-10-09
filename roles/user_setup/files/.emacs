;; enable syntax highlighting
(global-font-lock-mode 1)
;; show line and column numbers in mode line
(line-number-mode 1)
(column-number-mode 1)
;; force emacs to always use spaces instead of tab characters
(setq-default indent-tabs-mode nil)
;; set default tab width to 4 spaces
(setq default-tab-width 4)
(setq tab-width 4)
;; default to showing trailing whitespace
(setq-default show-trailing-whitespace t)
;; default to auto-fill-mode on in all major modes
(setq-default auto-fill-function 'do-auto-fill)
;; add a rust mode
(require 'rust-mode)
;; treat .hip files as .cpp
(add-to-list 'auto-mode-alist '("\\.hip\\'" . c++-mode))
