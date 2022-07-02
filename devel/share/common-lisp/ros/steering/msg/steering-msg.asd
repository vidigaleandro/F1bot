
(cl:in-package :asdf)

(defsystem "steering-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "steer" :depends-on ("_package_steer"))
    (:file "_package_steer" :depends-on ("_package"))
  ))