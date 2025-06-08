from fastapi import APIRouter, Query
from utils.dbutils import get_data_from_db

router = APIRouter()


def fetch_tracking_info(table_name: str, tracking_number: str):
    """
    Generic function to fetch tracking info from a given table.
    """
    query = f"SELECT * FROM data.{table_name} WHERE trackingnumber = :value"
    return get_data_from_db(query, tracking_number)


@router.get("/containers")
def get_container_info(container_number: str = Query(..., min_length=3)):
    """
    Get container tracking info by container number.
    """
    result = fetch_tracking_info("containers", container_number)
    return {"results": result}


@router.get("/bill-of-lading")
def get_bol_info(bill_of_lading_number: str = Query(..., min_length=3)):
    """
    Get bill of lading tracking info by BOL number.
    """
    result = fetch_tracking_info("bill_of_lading", bill_of_lading_number)
    return {"results": result}