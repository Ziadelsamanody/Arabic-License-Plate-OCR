from fastapi import APIRouter
import torch

router = APIRouter()

@router.get('/health')
async def health():
    return {
        'status' : 'working',
        'device': 'cuda' if torch.cuda.is_available() else 'cpu'
    }
