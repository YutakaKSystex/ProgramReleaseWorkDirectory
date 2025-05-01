from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.utils.auth import get_current_user
from app.schemas.schemas import (
    ApprovalRouteCreate, ApprovalRouteResponse, ApprovalRouteUpdate
)
from app.services.database import (
    create_approval_route, get_approval_route_by_id, get_all_approval_routes,
    update_approval_route, delete_approval_route
)
from app.models.models import User, UserRole

router = APIRouter(
    prefix="/approval-routes",
    tags=["approval routes"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=ApprovalRouteResponse)
async def create_new_approval_route(
    route: ApprovalRouteCreate, 
    current_user: User = Depends(get_current_user)
):
    new_route = create_approval_route(
        name=route.name,
        created_by=current_user.id,
        description=route.description,
        steps=route.steps
    )
    
    return new_route


@router.get("/", response_model=List[ApprovalRouteResponse])
async def read_approval_routes(current_user: User = Depends(get_current_user)):
    routes = get_all_approval_routes()
    
    return routes


@router.get("/{route_id}", response_model=ApprovalRouteResponse)
async def read_approval_route(route_id: str, current_user: User = Depends(get_current_user)):
    route = get_approval_route_by_id(route_id)
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    return route


@router.put("/{route_id}", response_model=ApprovalRouteResponse)
async def update_approval_route_info(
    route_id: str, 
    route_data: ApprovalRouteUpdate, 
    current_user: User = Depends(get_current_user)
):
    route = get_approval_route_by_id(route_id)
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    if route.created_by != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this route"
        )
    
    update_data = route_data.dict(exclude_unset=True)
    updated_route = update_approval_route(route_id, **update_data)
    
    return updated_route


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_approval_route_item(route_id: str, current_user: User = Depends(get_current_user)):
    route = get_approval_route_by_id(route_id)
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    if route.created_by != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this route"
        )
    
    delete_approval_route(route_id)
    
    return None
