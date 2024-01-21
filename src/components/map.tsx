'use client'
import 'leaflet/dist/leaflet.css'

import { MapContainer, TileLayer } from 'react-leaflet'


const Map = () => {
    const position: [number, number] = [51.505, -0.09]
  return (
    <MapContainer center={position} zoom={13} scrollWheelZoom={true} style={{height: 400, width: "100%"}}>
      <TileLayer
        attribution='&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png"
      />
    </MapContainer>
  )
}

export default Map