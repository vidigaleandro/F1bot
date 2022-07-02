; Auto-generated. Do not edit!


(cl:in-package steering-msg)


;//! \htmlinclude steer.msg.html

(cl:defclass <steer> (roslisp-msg-protocol:ros-message)
  ((a
    :reader a
    :initarg :a
    :type cl:float
    :initform 0.0))
)

(cl:defclass steer (<steer>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <steer>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'steer)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name steering-msg:<steer> is deprecated: use steering-msg:steer instead.")))

(cl:ensure-generic-function 'a-val :lambda-list '(m))
(cl:defmethod a-val ((m <steer>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader steering-msg:a-val is deprecated.  Use steering-msg:a instead.")
  (a m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <steer>) ostream)
  "Serializes a message object of type '<steer>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'a))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <steer>) istream)
  "Deserializes a message object of type '<steer>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'a) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<steer>)))
  "Returns string type for a message object of type '<steer>"
  "steering/steer")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'steer)))
  "Returns string type for a message object of type 'steer"
  "steering/steer")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<steer>)))
  "Returns md5sum for a message object of type '<steer>"
  "3a9a8ccf1ae2be3477477819c0d93b4e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'steer)))
  "Returns md5sum for a message object of type 'steer"
  "3a9a8ccf1ae2be3477477819c0d93b4e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<steer>)))
  "Returns full string definition for message of type '<steer>"
  (cl:format cl:nil "float32 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'steer)))
  "Returns full string definition for message of type 'steer"
  (cl:format cl:nil "float32 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <steer>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <steer>))
  "Converts a ROS message object to a list"
  (cl:list 'steer
    (cl:cons ':a (a msg))
))
