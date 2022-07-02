;; Auto-generated. Do not edit!


(when (boundp 'steering::steer)
  (if (not (find-package "STEERING"))
    (make-package "STEERING"))
  (shadow 'steer (find-package "STEERING")))
(unless (find-package "STEERING::STEER")
  (make-package "STEERING::STEER"))

(in-package "ROS")
;;//! \htmlinclude steer.msg.html


(defclass steering::steer
  :super ros::object
  :slots (_a ))

(defmethod steering::steer
  (:init
   (&key
    ((:a __a) 0.0)
    )
   (send-super :init)
   (setq _a (float __a))
   self)
  (:a
   (&optional __a)
   (if __a (setq _a __a)) _a)
  (:serialization-length
   ()
   (+
    ;; float32 _a
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _a
       (sys::poke _a (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _a
     (setq _a (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get steering::steer :md5sum-) "3a9a8ccf1ae2be3477477819c0d93b4e")
(setf (get steering::steer :datatype-) "steering/steer")
(setf (get steering::steer :definition-)
      "float32 a

")



(provide :steering/steer "3a9a8ccf1ae2be3477477819c0d93b4e")


