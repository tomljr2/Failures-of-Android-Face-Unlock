package com.example.researchapp

import android.app.Activity
import android.widget.TextView
import android.widget.Toast
import com.example.researchapp.models.FaceBounds
import com.example.researchapp.models.Frame
import com.google.firebase.ml.vision.common.FirebaseVisionImage
import com.google.firebase.ml.vision.common.FirebaseVisionImageMetadata
import com.google.firebase.ml.vision.face.FirebaseVisionFace


class FaceDetector(private val faceBoundsOverlay: FaceBoundsOverlay) {

    private val faceBoundsOverlayHandler = FaceBoundsOverlayHandler()
    private val firebaseFaceDetectorWrapper = FirebaseFaceDetectorWrapper()

    fun process(frame: Frame) {
        updateOverlayAttributes(frame)
        detectFacesIn(frame)
    }

    private fun updateOverlayAttributes(frame: Frame) {
        faceBoundsOverlayHandler.updateOverlayAttributes(
                overlayWidth = frame.size.width,
                overlayHeight = frame.size.height,
                rotation = frame.rotation,
                isCameraFacingBack = frame.isCameraFacingBack,
                callback = { newWidth, newHeight, newOrientation, newFacing ->
                    faceBoundsOverlay.cameraPreviewWidth = newWidth
                    faceBoundsOverlay.cameraPreviewHeight = newHeight
                    faceBoundsOverlay.cameraOrientation = newOrientation
                    faceBoundsOverlay.cameraFacing = newFacing
                })
    }

    private fun detectFacesIn(frame: Frame): MutableList<FaceBounds> {
        var faceBounds=mutableListOf<FaceBounds>()
        frame.data?.let {
            firebaseFaceDetectorWrapper.process(
                    image = convertFrameToImage(frame),
                    onSuccess = {
                        faceBounds=faceBoundsOverlay.updateFaces(convertToListOfFaceBounds(it))
                        if (faceBounds.isNotEmpty())
                           MainActivity.textView.setText(faceBounds[0].box.height().toString())
                    },
                    onError = {
                        Toast.makeText(faceBoundsOverlay.context, "Error processing images: $it", Toast.LENGTH_LONG).show()
                    })
        }
        return faceBounds
    }

    private fun convertFrameToImage(frame: Frame) =
            FirebaseVisionImage.fromByteArray(frame.data!!, extractFrameMetadata(frame))

    private fun extractFrameMetadata(frame: Frame): FirebaseVisionImageMetadata =
            FirebaseVisionImageMetadata.Builder()
                    .setWidth(frame.size.width)
                    .setHeight(frame.size.height)
                    .setFormat(frame.format)
                    .setRotation(frame.rotation / RIGHT_ANGLE)
                    .build()

    private fun convertToListOfFaceBounds(faces: MutableList<FirebaseVisionFace>): List<FaceBounds> =
            faces.map { FaceBounds(it.trackingId, it.boundingBox) }

    companion object {
        private const val RIGHT_ANGLE = 90
    }
}