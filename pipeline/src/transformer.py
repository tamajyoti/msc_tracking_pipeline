from typing import Tuple, List, Dict
from utils.pipeline_utils import generate_hash_id
from src.api_client import fetch_tracking_info
from utils.db_utils import insert_records


def transform_response(response_data: dict) -> Tuple[List[Dict], List[Dict]]:
    """
    Transforms API response JSON into structured records for database insertion.

    Args:
        response_data (dict): JSON response from the tracking API.

    Returns:
        Tuple[List[Dict], List[Dict]]: A tuple of lists:
            - Bill of lading records
            - Container tracking records
    """
    tracking_type = response_data['Data']['TrackingType']
    tracking_number = response_data['Data']['TrackingNumber']

    bill_of_lading_records = []
    container_records = []

    for bol in response_data['Data']['BillOfLadings']:
        # Construct bill of lading record
        bol_record = {
            "TrackingType": tracking_type,
            "TrackingNumber": tracking_number,
            "NumberOfContainers": bol['NumberOfContainers'],
            "BillOfLadingNumber": bol['BillOfLadingNumber'],
            "ShippedFrom": bol['GeneralTrackingInfo']['ShippedFrom'],
            "ShippedTo": bol['GeneralTrackingInfo']['ShippedTo'],
            "PortOfLoad": bol['GeneralTrackingInfo']['PortOfLoad'],
            "PortOfDischarge": bol['GeneralTrackingInfo']['PortOfDischarge'],
            "PriceCalculationDate": bol['GeneralTrackingInfo']['PriceCalculationDate'],
            "FinalPodEtaDate": bol['GeneralTrackingInfo']['FinalPodEtaDate'],
        }
        bol_record["id"] = generate_hash_id(bol_record)
        bill_of_lading_records.append(bol_record)

        # Construct container records per event
        for container in bol['ContainersInfo']:
            for event in container["Events"]:
                container_record = {
                    "TrackingType": tracking_type,
                    "TrackingNumber": tracking_number,
                    "BillOfLadingNumber": bol['BillOfLadingNumber'],
                    "ShippedFrom": bol['GeneralTrackingInfo']['ShippedFrom'],
                    "ShippedTo": bol['GeneralTrackingInfo']['ShippedTo'],
                    "PortOfLoad": bol['GeneralTrackingInfo']['PortOfLoad'],
                    "PortOfDischarge": bol['GeneralTrackingInfo']['PortOfDischarge'],
                    "PriceCalculationDate": bol['GeneralTrackingInfo']['PriceCalculationDate'],
                    "FinalPodEtaDate": bol['GeneralTrackingInfo']['FinalPodEtaDate'],
                    "OrderNo": event['Order'],
                    "Date": event['Date'],
                    "Location": event['Location'],
                    "Description": event['Description'],
                    "ContainerNumber": container['ContainerNumber'],
                    "Delivered": container['Delivered'],
                    "PodEtaDate": container['PodEtaDate'],
                    "ContainerType": container['ContainerType'],
                    "LatestMove": container['LatestMove']
                }
                container_record["id"] = generate_hash_id(container_record)
                container_records.append(container_record)

    return bill_of_lading_records, container_records


def process_tracking_number(tracking_number: str) -> None:
    """
    Fetches and processes tracking data for a given tracking number, inserting results into the database.

    Args:
        tracking_number (str): The container or bill of lading tracking number to be fetched and processed.
    """
    print(f"\n🔍 Processing tracking number: {tracking_number}")
    response = fetch_tracking_info(tracking_number)

    bol_records, container_records = transform_response(response)

    insert_records("bill_of_lading", bol_records)
    insert_records("containers", container_records)

    print(f"✅ Finished processing: {tracking_number}")
